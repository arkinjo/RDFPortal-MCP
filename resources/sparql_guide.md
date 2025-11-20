# SPARQL Query Guide

## The Golden Rule
**Before writing any query:** Can you draw a connected graph of all variables using predicates from the schema? If no → the query will fail or produce false results.

---

## The 3-Step Process

### 1. Check Available Databases
```
Run: list_databases()
```

### 2. Read the Schema & Statistics (MANDATORY)
```
Run: get_MIE_file(database_name)
```

**Extract from the MIE file:**

| Section | What to Find | How to Use It |
|---------|--------------|---------------|
| **Shape expressions** | Connecting predicates | Build graph connections |
| **Total counts** | Dataset sizes | Decide if filtering is mandatory |
| **Coverage (%)** | Property availability | Use direct vs OPTIONAL |
| **Cardinality** | avg/max relationships | Expect result multiplication, use DISTINCT |
| **Performance** | Required filters | Apply FIRST - prevents timeouts |
| **Examples** | Query patterns | Follow proven templates |

**Key statistics example (UniProt):**
```yaml
total_proteins: "444M → reviewed_proteins: 923K (0.2%)"
# Performance note: "ESSENTIAL - Use up:reviewed 1 for all queries"
# Coverage: function_annotations >90%, pdb_structures ~15%
# Cardinality: avg 12.5 GO terms per protein
```

### 3. Build Connected Queries

```sparql
SELECT ?var1 ?var2
WHERE {
  # 1. Required filters FIRST (from performance section)
  ?var1 required_filter "value" .
  
  # 2. Connections (from shape expressions)
  ?var1 connects_to ?var2 .
  
  # 3. Properties based on coverage
  ?var1 high_coverage_prop ?value .              # >85%: direct
  OPTIONAL { ?var1 low_coverage_prop ?opt }      # <50%: optional
  
  # 4. Filters last
  FILTER(...)
}
LIMIT 50  # Adjust for expected cardinality
```

---

## Common Mistakes

### ❌ Disconnected Variables
```sparql
WHERE {
  ?gene a Gene .
  ?protein a Protein .  # No connection!
}
# Result: gene × protein = Cartesian product
```

### ❌ Missing Required Filters
```sparql
# Will timeout on UniProt
SELECT (COUNT(*) as ?count)
WHERE { ?protein a up:Protein . }
```

### ✅ Correct Pattern
```sparql
WHERE {
  ?protein up:reviewed 1 ;          # Required filter first
           encodesBy ?gene .        # Connection from schema
}
```

---

## Query Development

**Process:**
1. Check statistics → identify required filters & coverage
2. Apply required filters first
3. Start simple, add one connection at a time
4. Set LIMIT based on cardinality (avg × expected matches)

**When presenting queries:**
- Show connection path: `?a → (predicate) → ?b`
- Note required filters and their source (performance section)
- Estimate result size using statistics

**Example using statistics:**
```sparql
# Scenario: Human DNA repair proteins
# Statistics: 40K human reviewed, 1.5K DNA repair total, >90% have functions

PREFIX up: <http://purl.uniprot.org/core/>
SELECT ?protein ?function
WHERE {
  ?protein up:reviewed 1 ;                                    # Required
           up:organism <http://purl.uniprot.org/taxonomy/9606> ;
           up:annotation ?annot .
  ?annot a up:Function_Annotation ;
         rdfs:comment ?function .
  FILTER(CONTAINS(LCASE(?function), "dna repair"))
}
LIMIT 30  # Expect ~200-500 matches, 30 is reasonable sample
```

---

## Red Flags - Stop If:

- Variables have no connecting predicates
- Variables only share literal values
- You haven't read the MIE file
- You skipped required filters from performance section
- Result count >> expected from cardinality
- Using direct properties for low-coverage data (<50%)

---

## If Results Look Wrong

**Check:**
1. Are connections from schema correct?
2. Did I apply required performance filters?
3. Is result count consistent with coverage × cardinality?
4. Should low-coverage properties be OPTIONAL?

**Example diagnostic:**
```
Query returns 0 results for PDB structures:
→ Check statistics: coverage ~15% for reviewed proteins
→ Fix: Make PDB property OPTIONAL or accept sparse results
```

---

## Statistics Checklist

Before querying, extract from MIE's `data_statistics` section:

- [ ] Required filters (performance_characteristics)
- [ ] Total counts (scale of dataset)
- [ ] Coverage % (direct vs OPTIONAL)
- [ ] Cardinality avg/max (result multiplication)

---

## Quick Reference

| Do | Don't |
|----|-------|
| Read MIE file first | Guess predicates |
| Apply required filters first | Skip performance filters |
| Use statistics for LIMIT | Use arbitrary numbers |
| OPTIONAL for <50% coverage | OPTIONAL for >85% coverage |
| Connect via predicates | Connect via shared literals |

**Remember:** 
- Required filters are non-negotiable
- Coverage % determines direct vs OPTIONAL
- Cardinality predicts result sizes
- Empty results > false positives