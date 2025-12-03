# RDF Portal MCP Server Evaluation Framework

## Overview

This evaluation framework contains **30 biologically relevant questions** designed to assess the effectiveness of the RDF Portal MCP Server. The questions are specifically designed to test scenarios where the RDF Portal provides **genuine added value** over an LLM's inherent knowledge.

## Core Principle: Why RDF Portal?

Each question is designed to highlight one of five key value propositions:

| Value Type | Description | Example |
|------------|-------------|---------|
| **Quantitative Precision** | Exact counts/values vs. estimates | "How many reviewed human proteins?" |
| **Exhaustive Enumeration** | Complete lists vs. examples | "List ALL approved melanoma drugs" |
| **Multi-Criteria Filtering** | Complex database queries | "Kinase inhibitors with IC50 < 10nM" |
| **Cross-Database Integration** | Linking disparate data | "UniProt → PDB → Pathways" |
| **Verification** | Fact-checking against authority | "Is BRCA1 annotated for DNA repair?" |

## Question Distribution

### By Category
```
Quantitative:     7 questions (23%)
Enumeration:      6 questions (20%)
Multi-criteria:   8 questions (27%)
Cross-database:   4 questions (13%)
Verification:     5 questions (17%)
```

### By Difficulty
```
Easy:    8 questions (27%)
Medium: 12 questions (40%)
Hard:   10 questions (33%)
```

### By Database
```
UniProt:   10 questions (33%)
ChEMBL:    10 questions (33%)
PDB:        6 questions (20%)
GO:         3 questions (10%)
Reactome:   5 questions (17%)
```
*(Some questions use multiple databases)*

## Verified Ground Truth Examples

Several questions have been validated with actual SPARQL queries:

| Question | Ground Truth | Source |
|----------|--------------|--------|
| Reviewed human proteins in UniProt | **20,435** | SPARQL verified |
| Approved drugs in ChEMBL | **3,592** | SPARQL verified |
| Cryo-EM structures in PDB | **15,032** | SPARQL verified |
| Human pathways in Reactome | **2,673** | SPARQL verified |
| Best resolution structure | **0.48 Å** (5D8V, 3NIR) | SPARQL verified |
| Imatinib Kd for ABL | **1.0-6.0 nM** | SPARQL verified |
| Imatinib approval status | **Phase 4** (CHEMBL941) | SPARQL verified |

## How to Use This Evaluation

### For Each Question:

1. **Present the question** to the system
2. **Record the tools called** (get_MIE_file, run_sparql, etc.)
3. **Evaluate the SPARQL query** (if generated)
4. **Compare answer to ground truth**
5. **Score on criteria:**
   - Correctness: Is the answer factually correct?
   - Completeness: Are all relevant results returned?
   - Query Efficiency: Was the query well-formed?

### Scoring Guidelines

| Score | Description |
|-------|-------------|
| 3 | Fully correct, complete, efficient query |
| 2 | Mostly correct, minor omissions or inefficiencies |
| 1 | Partially correct, significant issues |
| 0 | Incorrect or failed to execute |

## Sample Evaluation Workflow

```
Question: "How many approved drugs are in ChEMBL?"

Step 1: System should call get_MIE_file for ChEMBL
Step 2: System should construct SPARQL:
        SELECT (COUNT(DISTINCT ?molecule) as ?count)
        WHERE { ?molecule cco:highestDevelopmentPhase 4 }
Step 3: System should return: 3,592
Step 4: Compare to ground truth: 3,592 ✓
Step 5: Score: 3/3
```

## Key Technical Patterns to Test

### UniProt
- Must use `up:reviewed 1` for quality filtering
- Must use `bif:contains` for text search
- Must use taxonomy URIs for organism filtering

### ChEMBL
- Must include `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
- Must use `bif:contains` with proper syntax
- Must filter units when comparing activity values

### PDB
- Must use `FROM <http://rdfportal.org/dataset/pdbj>`
- Must cast resolution values for numeric comparison
- Must join multiple category paths for complete data

### GO
- Must filter by `STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_")`
- Must use `DISTINCT` to avoid duplicates
- Must use `bif:contains` for keyword search

### Reactome
- Must use `STR()` for ALL string comparisons
- Must include `FROM <http://rdf.ebi.ac.uk/dataset/reactome>`
- Must navigate BioPAX property paths

## Expected Challenges

1. **Query timeouts** - Some complex queries may timeout
2. **Empty results** - Incorrect patterns return nothing
3. **Duplicate results** - Missing DISTINCT clause
4. **Type mismatches** - String vs. numeric comparisons
5. **Missing filters** - Unbounded queries on large datasets

## Files

- `rdf_portal_evaluation_qa.yaml` - Full question set with ground truth
- This document (`README.md`) - Framework explanation

---

*Framework version 1.0 - Created 2025-01-27*