# RDF Portal MCP Server - Evaluation Framework

This directory contains a comprehensive evaluation framework for validating the effectiveness of the RDF Portal MCP Server.

## Overview

The evaluation compares:
- **Baseline**: LLM (Claude) answering questions without any tools
- **Treatment**: LLM (Claude) with RDF Portal MCP tools enabled
- **Ground Truth**: Verified correct answers from database queries

## Files

| File | Description |
|------|-------------|
| `execution_guide.md` | Step-by-step guide for running the validation |
| `recording_sheet.csv` | CSV template for recording results (30 questions) |
| `recording_template.tsv` | TSV template with more detail |
| `verify_ground_truth.md` | SPARQL queries to verify expected answers |
| `scoring_rubrics.yaml` | Detailed scoring criteria by question type |
| `execution_protocol.yaml` | Full protocol specification |
| `ground_truth_template.yaml` | Template for documenting ground truth |
| `analyze_validation.py` | Python script to analyze results and generate report |

## Quick Start

1. **Verify ground truth** (optional but recommended):
   ```bash
   # Run queries in verify_ground_truth.md using RDF Portal
   ```

2. **Run validation**:
   - Follow `execution_guide.md`
   - Record results in `recording_sheet.csv`

3. **Analyze results**:
   ```bash
   python analyze_validation.py recording_sheet.csv report.md
   ```

## Question Categories

| Category | Count | Description |
|----------|-------|-------------|
| Quantitative | 7 | Exact counts and values |
| Enumeration | 7 | Complete lists |
| Multi-criteria | 8 | Complex filtering |
| Cross-database | 4 | Integration across sources |
| Verification | 4 | Fact-checking |

## Difficulty Distribution

| Difficulty | Count |
|------------|-------|
| Easy | 8 |
| Medium | 12 |
| Hard | 10 |

## Expected Results (from preliminary testing)

| Metric | Baseline | Treatment |
|--------|----------|-----------|
| Mean Score | ~2.2/3 (73%) | ~2.9/3 (96%) |
| Perfect Scores | ~33% | ~87% |
| Improvement | — | +23% |

## Scoring Scale

- **3**: Exact/complete/verified
- **2**: Close/mostly correct
- **1**: Partial
- **0**: Failed/incorrect

## Value Added Categories

- `precision`: Exact value vs. estimate
- `completeness`: Full list vs. examples
- `capability`: Possible vs. impossible without tools
- `verification`: Confirmed vs. assumed
- `none`: No improvement

## Time Estimate

- **Full validation**: 4-6 hours
- **Quick validation** (easy questions only): 1 hour

## Requirements

For analysis script:
```bash
pip install pandas numpy
```
