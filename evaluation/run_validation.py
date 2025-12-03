#!/usr/bin/env python3
"""
RDF Portal Validation Runner with Timing
=========================================
Automates the validation process and measures execution times.

Requirements:
    pip install anthropic pandas

Usage:
    # Set your API key
    export ANTHROPIC_API_KEY="your-key-here"
    
    # Run validation
    python run_validation.py
"""

import os
import sys
import time
import json
import pandas as pd
from datetime import datetime
from typing import Optional

try:
    import anthropic
except ImportError:
    print("Please install anthropic: pip install anthropic")
    sys.exit(1)

# Configuration
MODEL = "claude-sonnet-4-20250514"  # or claude-3-opus, etc.
MAX_TOKENS = 4096

# Questions to test
QUESTIONS = [
    {"id": "Q001", "question": "How many reviewed (Swiss-Prot) human proteins are in UniProt?", "category": "quantitative", "difficulty": "easy"},
    {"id": "Q002", "question": "How many approved (Phase 4) drugs are in ChEMBL?", "category": "quantitative", "difficulty": "easy"},
    {"id": "Q003", "question": "How many cryo-EM structures are in PDB?", "category": "quantitative", "difficulty": "easy"},
    {"id": "Q004", "question": "How many human pathways are curated in Reactome?", "category": "quantitative", "difficulty": "easy"},
    {"id": "Q005", "question": "What is the best (highest) resolution protein structure in PDB?", "category": "quantitative", "difficulty": "medium"},
    {"id": "Q006", "question": "List all approved (Phase 4) drugs indicated for melanoma", "category": "enumeration", "difficulty": "medium"},
    {"id": "Q007", "question": "List all GO molecular function terms containing 'kinase' in the name", "category": "enumeration", "difficulty": "medium"},
    {"id": "Q009", "question": "What is the binding affinity (Kd) of imatinib for ABL kinase?", "category": "multi_criteria", "difficulty": "medium"},
    {"id": "Q013", "question": "For UniProt protein P04637 (p53), what PDB structures are available?", "category": "cross_database", "difficulty": "medium"},
    {"id": "Q015", "question": "What pathways in Reactome involve the protein p53 (TP53)?", "category": "cross_database", "difficulty": "hard"},
    {"id": "Q017", "question": "Is imatinib (Gleevec) approved as a drug? What is its development phase?", "category": "verification", "difficulty": "easy"},
    {"id": "Q018", "question": "Is BRCA1 annotated as involved in DNA repair in UniProt?", "category": "verification", "difficulty": "easy"},
    {"id": "Q021", "question": "What is the molecular weight of the p53 protein according to UniProt?", "category": "quantitative", "difficulty": "medium"},
    {"id": "Q022", "question": "What experimental methods have been used to determine ribosome structures?", "category": "enumeration", "difficulty": "medium"},
    {"id": "Q027", "question": "List all organisms represented in Reactome pathways", "category": "enumeration", "difficulty": "easy"},
]

class TimedResponse:
    """Wrapper for API response with timing information."""
    def __init__(self, response_text: str, elapsed_time: float, tool_calls: int = 0):
        self.text = response_text
        self.elapsed_time = elapsed_time
        self.tool_calls = tool_calls

def run_baseline_query(client: anthropic.Anthropic, question: str) -> TimedResponse:
    """Run a query without tools (baseline)."""
    prompt = f"""Please answer this question using only your knowledge:

{question}

Give your best answer. If you need to estimate, provide your estimate."""

    start_time = time.time()
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )
    
    elapsed = time.time() - start_time
    
    return TimedResponse(
        response_text=response.content[0].text,
        elapsed_time=elapsed,
        tool_calls=0
    )

def run_treatment_query_simulation(client: anthropic.Anthropic, question: str) -> TimedResponse:
    """
    Simulate treatment query timing.
    
    Note: For actual MCP tool usage, you would need to:
    1. Connect to the RDF Portal MCP server
    2. Use the tools in the API call
    
    This is a placeholder that estimates timing based on baseline + overhead.
    """
    prompt = f"""Please answer this question. Imagine you have access to RDF Portal tools 
and can query UniProt, ChEMBL, PDB, GO, and Reactome databases using SPARQL.

{question}

Describe what query you would run and what the expected result would be."""

    start_time = time.time()
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )
    
    elapsed = time.time() - start_time
    
    # In real usage, you'd count actual tool calls
    estimated_tool_calls = 1 if "SPARQL" in response.content[0].text else 0
    
    return TimedResponse(
        response_text=response.content[0].text,
        elapsed_time=elapsed,
        tool_calls=estimated_tool_calls
    )

def run_validation(questions: list, output_file: str = "validation_results.csv"):
    """Run the full validation suite with timing."""
    
    # Initialize client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    results = []
    
    print(f"Starting validation of {len(questions)} questions...")
    print("=" * 60)
    
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {q['id']}: {q['question'][:50]}...")
        
        # Run baseline
        print("  Running baseline...", end=" ", flush=True)
        baseline = run_baseline_query(client, q['question'])
        print(f"Done ({baseline.elapsed_time:.1f}s)")
        
        # Small delay to avoid rate limiting
        time.sleep(1)
        
        # Run treatment (simulation)
        print("  Running treatment...", end=" ", flush=True)
        treatment = run_treatment_query_simulation(client, q['question'])
        print(f"Done ({treatment.elapsed_time:.1f}s)")
        
        # Record results
        results.append({
            "question_id": q['id'],
            "question": q['question'],
            "category": q['category'],
            "difficulty": q['difficulty'],
            "baseline_answer": baseline.text[:500],  # Truncate for CSV
            "baseline_time_sec": round(baseline.elapsed_time, 2),
            "treatment_answer": treatment.text[:500],
            "treatment_time_sec": round(treatment.elapsed_time, 2),
            "tool_calls": treatment.tool_calls,
            "timestamp": datetime.now().isoformat()
        })
        
        # Small delay between questions
        time.sleep(2)
    
    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print(f"Validation complete! Results saved to {output_file}")
    
    # Print summary
    print("\nTiming Summary:")
    print(f"  Baseline mean: {df['baseline_time_sec'].mean():.1f}s")
    print(f"  Treatment mean: {df['treatment_time_sec'].mean():.1f}s")
    print(f"  Total baseline time: {df['baseline_time_sec'].sum():.1f}s")
    print(f"  Total treatment time: {df['treatment_time_sec'].sum():.1f}s")
    
    return df

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "validation_results.csv"
    run_validation(QUESTIONS, output)
