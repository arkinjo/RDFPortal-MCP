#!/usr/bin/env python3
"""
RDF Portal MCP Server Validation Analysis
==========================================
Analyzes validation results and generates comprehensive report.

Usage:
    python analyze_validation.py recording_template.tsv output_report.md
"""

import sys
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime

def load_data(filepath):
    """Load validation results from TSV file."""
    df = pd.read_csv(filepath, sep='\t')
    return df

def calculate_scores(df):
    """Calculate summary statistics."""
    results = {}
    
    # Overall scores
    results['overall'] = {
        'baseline_mean': df['baseline_score'].mean(),
        'treatment_mean': df['treatment_score'].mean(),
        'improvement': df['treatment_score'].mean() - df['baseline_score'].mean(),
        'improvement_pct': ((df['treatment_score'].mean() - df['baseline_score'].mean()) / 
                           df['baseline_score'].mean() * 100) if df['baseline_score'].mean() > 0 else 0
    }
    
    # By category
    results['by_category'] = {}
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        results['by_category'][category] = {
            'n': len(cat_df),
            'baseline_mean': cat_df['baseline_score'].mean(),
            'treatment_mean': cat_df['treatment_score'].mean(),
            'improvement': cat_df['treatment_score'].mean() - cat_df['baseline_score'].mean()
        }
    
    # By difficulty
    results['by_difficulty'] = {}
    for difficulty in df['difficulty'].unique():
        diff_df = df[df['difficulty'] == difficulty]
        results['by_difficulty'][difficulty] = {
            'n': len(diff_df),
            'baseline_mean': diff_df['baseline_score'].mean(),
            'treatment_mean': diff_df['treatment_score'].mean(),
            'improvement': diff_df['treatment_score'].mean() - diff_df['baseline_score'].mean()
        }
    
    # Success rates
    results['success_rates'] = {
        'baseline_perfect': (df['baseline_score'] == 3).sum() / len(df) * 100,
        'treatment_perfect': (df['treatment_score'] == 3).sum() / len(df) * 100,
        'baseline_failed': (df['baseline_score'] <= 1).sum() / len(df) * 100,
        'treatment_failed': (df['treatment_score'] <= 1).sum() / len(df) * 100
    }
    
    return results

def analyze_value_added(df):
    """Analyze types of value added by RDF Portal."""
    value_types = df['value_added_type'].value_counts().to_dict()
    
    # Questions where treatment outperformed baseline
    improved = df[df['treatment_score'] > df['baseline_score']]
    
    # Questions where baseline matched or beat treatment
    no_improvement = df[df['treatment_score'] <= df['baseline_score']]
    
    return {
        'value_types': value_types,
        'improved_count': len(improved),
        'no_improvement_count': len(no_improvement),
        'improved_questions': improved['question_id'].tolist(),
        'no_improvement_questions': no_improvement['question_id'].tolist()
    }

def analyze_errors(df):
    """Analyze error patterns."""
    errors = df['errors_encountered'].dropna()
    error_counts = defaultdict(int)
    
    for error_str in errors:
        if pd.notna(error_str) and error_str:
            for error in str(error_str).split(';'):
                error_counts[error.strip()] += 1
    
    return dict(error_counts)

def analyze_tool_usage(df):
    """Analyze tool usage patterns."""
    tools = df['tools_used'].dropna()
    tool_counts = defaultdict(int)
    
    for tool_str in tools:
        if pd.notna(tool_str) and tool_str:
            for tool in str(tool_str).split(';'):
                tool_counts[tool.strip()] += 1
    
    sparql_attempts = df['sparql_attempts'].dropna()
    
    return {
        'tool_usage': dict(tool_counts),
        'mean_sparql_attempts': sparql_attempts.mean() if len(sparql_attempts) > 0 else 0,
        'max_sparql_attempts': sparql_attempts.max() if len(sparql_attempts) > 0 else 0,
        'first_attempt_success': (sparql_attempts == 1).sum() if len(sparql_attempts) > 0 else 0
    }

def generate_report(df, results, value_analysis, error_analysis, tool_analysis):
    """Generate markdown report."""
    report = []
    
    report.append("# RDF Portal MCP Server Validation Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"\n**Total Questions:** {len(df)}")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append("| Metric | Baseline (No Tools) | Treatment (RDF Portal) | Improvement |")
    report.append("|--------|--------------------|-----------------------|-------------|")
    report.append(f"| Mean Score (out of 3) | {results['overall']['baseline_mean']:.2f} | {results['overall']['treatment_mean']:.2f} | +{results['overall']['improvement']:.2f} |")
    report.append(f"| Perfect Scores (3/3) | {results['success_rates']['baseline_perfect']:.1f}% | {results['success_rates']['treatment_perfect']:.1f}% | +{results['success_rates']['treatment_perfect'] - results['success_rates']['baseline_perfect']:.1f}% |")
    report.append(f"| Failed (0-1/3) | {results['success_rates']['baseline_failed']:.1f}% | {results['success_rates']['treatment_failed']:.1f}% | {results['success_rates']['treatment_failed'] - results['success_rates']['baseline_failed']:.1f}% |")
    report.append("")
    
    # By Category
    report.append("## Results by Category")
    report.append("")
    report.append("| Category | N | Baseline | Treatment | Improvement |")
    report.append("|----------|---|----------|-----------|-------------|")
    for cat, stats in results['by_category'].items():
        report.append(f"| {cat} | {stats['n']} | {stats['baseline_mean']:.2f} | {stats['treatment_mean']:.2f} | +{stats['improvement']:.2f} |")
    report.append("")
    
    # By Difficulty
    report.append("## Results by Difficulty")
    report.append("")
    report.append("| Difficulty | N | Baseline | Treatment | Improvement |")
    report.append("|------------|---|----------|-----------|-------------|")
    for diff in ['easy', 'medium', 'hard']:
        if diff in results['by_difficulty']:
            stats = results['by_difficulty'][diff]
            report.append(f"| {diff} | {stats['n']} | {stats['baseline_mean']:.2f} | {stats['treatment_mean']:.2f} | +{stats['improvement']:.2f} |")
    report.append("")
    
    # Value Added Analysis
    report.append("## Value Added Analysis")
    report.append("")
    report.append(f"- Questions where RDF Portal improved results: **{value_analysis['improved_count']}** ({value_analysis['improved_count']/len(df)*100:.1f}%)")
    report.append(f"- Questions with no improvement: **{value_analysis['no_improvement_count']}** ({value_analysis['no_improvement_count']/len(df)*100:.1f}%)")
    report.append("")
    
    if value_analysis['value_types']:
        report.append("### Value Added Types")
        report.append("")
        for vtype, count in sorted(value_analysis['value_types'].items(), key=lambda x: -x[1]):
            report.append(f"- {vtype}: {count} questions")
        report.append("")
    
    # Tool Usage
    report.append("## Tool Usage Analysis")
    report.append("")
    report.append(f"- Mean SPARQL attempts per question: **{tool_analysis['mean_sparql_attempts']:.1f}**")
    report.append(f"- First-attempt success rate: **{tool_analysis['first_attempt_success']}** questions")
    report.append(f"- Maximum attempts needed: **{tool_analysis['max_sparql_attempts']}**")
    report.append("")
    
    # Error Analysis
    if error_analysis:
        report.append("## Error Analysis")
        report.append("")
        for error, count in sorted(error_analysis.items(), key=lambda x: -x[1]):
            report.append(f"- {error}: {count} occurrences")
        report.append("")
    
    # Detailed Results
    report.append("## Detailed Results")
    report.append("")
    report.append("| ID | Category | Difficulty | Baseline | Treatment | Δ | Value Added |")
    report.append("|----|----------|------------|----------|-----------|---|-------------|")
    for _, row in df.iterrows():
        delta = row['treatment_score'] - row['baseline_score'] if pd.notna(row['treatment_score']) and pd.notna(row['baseline_score']) else 'N/A'
        if isinstance(delta, (int, float)):
            delta_str = f"+{delta}" if delta > 0 else str(delta)
        else:
            delta_str = delta
        report.append(f"| {row['question_id']} | {row['category']} | {row['difficulty']} | {row.get('baseline_score', 'N/A')} | {row.get('treatment_score', 'N/A')} | {delta_str} | {row.get('value_added_type', '')} |")
    report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    report.append("")
    report.append("Based on the validation results:")
    report.append("")
    report.append("1. **High-value use cases:** [To be filled based on results]")
    report.append("2. **Areas for improvement:** [To be filled based on error analysis]")
    report.append("3. **Query patterns that work well:** [To be filled based on success patterns]")
    report.append("4. **Query patterns that struggle:** [To be filled based on failure patterns]")
    report.append("")
    
    return '\n'.join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_validation.py <input.tsv> [output.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'validation_report.md'
    
    # Load data
    print(f"Loading data from {input_file}...")
    df = load_data(input_file)
    
    # Analyze
    print("Calculating scores...")
    results = calculate_scores(df)
    
    print("Analyzing value added...")
    value_analysis = analyze_value_added(df)
    
    print("Analyzing errors...")
    error_analysis = analyze_errors(df)
    
    print("Analyzing tool usage...")
    tool_analysis = analyze_tool_usage(df)
    
    # Generate report
    print("Generating report...")
    report = generate_report(df, results, value_analysis, error_analysis, tool_analysis)
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Baseline Mean Score: {results['overall']['baseline_mean']:.2f}/3")
    print(f"Treatment Mean Score: {results['overall']['treatment_mean']:.2f}/3")
    print(f"Improvement: +{results['overall']['improvement']:.2f} ({results['overall']['improvement_pct']:.1f}%)")
    print("="*60)

if __name__ == '__main__':
    main()
