# RDF Portal Guide - Concise with Verification Controls

## 🚨 MANDATORY WORKFLOW 🚨

```
1. get_MIE_file(dbname) → Extract statistics
2. PLAN strategy based on numbers  
3. COUNT with planned filters
4. EXECUTE with strategic LIMIT
5. VERIFY results match COUNT
6. CHUNK if truncated
7. REPORT with verification status
```

---

## STEP 1: EXTRACT STATISTICS

```yaml
total_entities: [NUMBER]
largest_class: [CLASS]: [NUMBER] 
indexed_properties: [LIST]
quality_tiers: [available/none]
```

**🚨 RED FLAGS**: >100K entities, >1M total, performance warnings

---

## STEP 2: STRATEGY

| Class Size | Strategy |
|------------|----------|
| <10K | Direct query, LIMIT 100 |
| 10K-100K | Quality filters + indexed properties |
| 100K-1M | Aggressive filtering + LIMIT ≤50 |
| >1M | Narrow scope + LIMIT ≤20 |

**Priority**: `reviewed=1` > `active=1` > unfiltered

---

## STEP 3: COUNT

```sparql
SELECT (COUNT(?entity) as ?count) WHERE {
  ?entity a [CLASS] ; [FILTERS] .
}
```

**COUNT → LIMIT**: <100: no limit, 100-200: LIMIT 100, >200: LIMIT 50

---

## STEP 4: EXECUTE

Execute main query with planned LIMIT.

---

## STEP 5: VERIFY ⬅️ CRITICAL

### Truncation Check
- "Result too long, truncated..."
- Incomplete rows
- Result count < COUNT

### Reconciliation
```yaml
Expected: [COUNT_NUMBER]
Retrieved: [ACTUAL_NUMBER]  
Status: [MATCH/MISMATCH]
```

**If MISMATCH**: STOP → Use chunking strategy

---

## STEP 6: CHUNKING (If Truncated)

### Two-Stage Approach
```sparql
-- Stage 1: Identifiers only
SELECT DISTINCT ?entity ?identifier 
WHERE { [filters] } ORDER BY ?identifier

-- Stage 2: Details in chunks  
SELECT ?entity ?identifier ?details
WHERE { VALUES ?identifier { "ID1" "ID2" ... } [filters] }
```

**Chunk sizes**: Text-heavy: 20, Simple: 50, Complex joins: 10

---

## STEP 7: REPORT

```yaml
COUNT Result: [NUMBER]
Retrieved: [NUMBER] 
Truncated: [YES/NO]
Strategy: [direct/chunked]
Final Answer: [NUMBER] ✓
```

---

## ERROR PREVENTION RULES

1. **COUNT is Gospel**: Final answer = COUNT result
2. **No Partial Analysis**: Truncated data = invalid results  
3. **Verify Everything**: Check reconciliation before summarizing

---

## COMPLIANCE CHECKLIST

**Pre-query:**
- [ ] Statistics documented: [NUMBERS]
- [ ] COUNT completed: [NUMBER]
- [ ] Strategy selected: [TYPE]

**Post-query:**
- [ ] Truncation checked: [YES/NO]
- [ ] Results match COUNT: [YES/NO]
- [ ] Complete data obtained: [YES/NO]

---

## QUICK REFERENCE

### Database Patterns
- **ChEMBL**: Filter `standardType`, LIMIT ≤100
- **UniProt**: `reviewed=1`, organism filters
- **MeSH/GO**: Use hierarchy, tree patterns
- **Reactome**: Filter organism early

### When to Chunk
- COUNT >50 + text-heavy results
- Any truncation detected
- Complex multi-table joins

### Emergency: Large Truncation
1. STOP analysis
2. Get identifiers only  
3. Chunk with size 20
4. Verify total = COUNT
5. Document strategy used

---

## CORE PRINCIPLE

**Use numbers, verify completeness, trust COUNT queries. Never analyze truncated data.**