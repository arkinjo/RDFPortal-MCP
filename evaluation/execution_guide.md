# RDF Portal Validation - Practical Execution Guide

## Before You Start

### Prerequisites Checklist
- [ ] Ground truth values verified (run queries in verify_ground_truth.md)
- [ ] Recording sheet ready (recording_sheet.csv)
- [ ] Timer/stopwatch available
- [ ] Two separate test environments ready

### Test Environment Setup

| Environment | Configuration | Purpose |
|-------------|---------------|---------|
| **Session A** | Claude WITHOUT MCP tools | Baseline measurement |
| **Session B** | Claude WITH RDF Portal MCP | Treatment measurement |

**Important:** Use fresh sessions for each question to avoid context contamination.

---

## Execution Protocol

### For EACH Question (30 total):

#### Part A: Baseline Test (No Tools)

1. **Open fresh Claude session WITHOUT MCP tools**

2. **Present the question with this exact prompt:**
   ```
   Please answer this question using only your knowledge:
   
   [INSERT QUESTION HERE]
   
   Give your best answer. If you need to estimate, provide your estimate.
   ```

3. **Record:**
   - Start timer when you send the question
   - Copy the full response to `baseline_answer`
   - Stop timer → record `baseline_time_sec`
   - Extract the key answer (number, list, yes/no)

4. **Score immediately using rubric:**
   - 3 = Exact/correct
   - 2 = Close/mostly correct  
   - 1 = Partial
   - 0 = Wrong/failed

#### Part B: Treatment Test (With RDF Portal)

1. **Open fresh Claude session WITH RDF Portal MCP**

2. **Present the question with this exact prompt:**
   ```
   Please answer this question using the RDF Portal tools:
   
   [INSERT QUESTION HERE]
   
   Use SPARQL queries to find the answer from the appropriate database(s).
   ```

3. **Record:**
   - Start timer when you send the question
   - Count SPARQL query attempts → `sparql_attempts`
   - Note any errors → `errors`
   - Copy final response to `treatment_answer`
   - Stop timer → record `treatment_time_sec`

4. **Score using same rubric**

5. **Classify value added:**
   - `precision` = Exact value vs estimate
   - `completeness` = Full list vs examples
   - `capability` = Possible vs impossible without tools
   - `verification` = Confirmed vs assumed
   - `none` = No improvement

---

## Scoring Rubrics (Quick Reference)

### Quantitative Questions (counts, values)
| Score | Criteria |
|-------|----------|
| 3 | Exact match or within 1% |
| 2 | Within 5% or correct magnitude |
| 1 | Within 20% |
| 0 | Off by >20% or failed |

### Enumeration Questions (lists)
| Score | Criteria |
|-------|----------|
| 3 | ≥95% recall, 100% precision |
| 2 | ≥80% recall, ≥95% precision |
| 1 | ≥50% recall, ≥80% precision |
| 0 | <50% recall or <80% precision |

### Multi-Criteria Questions (filtering)
| Score | Criteria |
|-------|----------|
| 3 | All criteria applied, correct results |
| 2 | Most criteria applied, mostly correct |
| 1 | Some criteria applied, partial results |
| 0 | Criteria not applied or failed |

### Verification Questions (fact-checking)
| Score | Criteria |
|-------|----------|
| 3 | Correct answer with evidence |
| 2 | Correct answer, weak evidence |
| 1 | Partially correct |
| 0 | Incorrect or no verification |

---

## Recommended Execution Order

Execute in batches to manage fatigue:

### Batch 1: Easy Questions (Warm-up)
**Time estimate: 45-60 minutes**

| Order | ID | Question |
|-------|-----|----------|
| 1 | Q001 | Reviewed human proteins count |
| 2 | Q002 | Approved drugs count |
| 3 | Q003 | Cryo-EM structures count |
| 4 | Q004 | Human pathways count |
| 5 | Q017 | Imatinib approval status |
| 6 | Q018 | BRCA1 DNA repair annotation |
| 7 | Q027 | Reactome organisms list |
| 8 | Q029 | GO apoptosis synonyms |

**☕ Take 10 minute break**

### Batch 2: Medium Questions (Core)
**Time estimate: 90-120 minutes**

| Order | ID | Question |
|-------|-----|----------|
| 9 | Q005 | Best resolution structure |
| 10 | Q006 | Melanoma drugs list |
| 11 | Q007 | GO kinase terms |
| 12 | Q009 | Imatinib Kd for ABL |
| 13 | Q012 | EGFR Phase 3+ drugs |
| 14 | Q013 | p53 PDB structures |
| 15 | Q019 | Aspirin COX-1 inhibition |
| 16 | Q020 | SARS-CoV-2 spike structures |
| 17 | Q021 | p53 molecular weight |
| 18 | Q022 | Ribosome structure methods |
| 19 | Q026 | Insulin sequence length |

**☕ Take 10 minute break**

### Batch 3: Hard Questions (Stress Test)
**Time estimate: 120-150 minutes**

| Order | ID | Question |
|-------|-----|----------|
| 20 | Q008 | Tumor suppressor proteins |
| 21 | Q010 | Kinase inhibitors IC50 <10nM |
| 22 | Q011 | Mitochondrial apoptosis proteins |
| 23 | Q014 | PDB-UniProt p53 mapping |
| 24 | Q015 | p53 Reactome pathways |
| 25 | Q016 | Glycolysis ChEBI compounds |
| 26 | Q023 | Kinase drugs for cancer |
| 27 | Q024 | GO component protein counts |
| 28 | Q025 | Top targeted proteins |
| 29 | Q028 | Small peptide NMR structures |
| 30 | Q030 | Multi-mechanism drugs |

---

## During Execution: What to Watch For

### Common Baseline (No Tools) Patterns
- Gives estimates instead of exact numbers
- Lists examples instead of complete enumerations
- Cannot perform systematic filtering
- May have outdated information
- Cannot verify claims against databases

### Common Treatment (RDF Portal) Patterns
- May need multiple query iterations
- Watch for timeout errors on complex queries
- Note when MIE file is consulted
- Track query patterns that work vs. fail

### Red Flags to Note
- Treatment takes significantly longer than baseline
- Treatment gives worse answer than baseline
- Query fails repeatedly (>5 attempts)
- Empty results when data should exist

---

## After Each Question

Fill in recording_sheet.csv immediately:

```csv
Q001,How many reviewed...,quantitative,easy,20435,"About 20000",2,15,"20435 (query result)",3,45,1,none,precision,"Exact vs estimate"
```

---

## Post-Validation Checklist

- [ ] All 30 questions completed
- [ ] All scores recorded (0-3)
- [ ] All times recorded
- [ ] All value_added types classified
- [ ] Notes captured for interesting cases
- [ ] CSV file saved

Then run analysis:
```bash
python analyze_validation.py recording_sheet.csv report.md
```
