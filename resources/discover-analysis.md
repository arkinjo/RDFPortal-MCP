# Discovery-First, Analysis-Second: Revised Methodology

## Core Principle
**Start broad with high-recall discovery, then progressively narrow with high-precision analysis.**

---

## The Five-Phase Framework

### Phase 1: Conceptual Mapping + Database Assessment
- Map key concepts using domain ontologies (OLS, BioPortal)
- Generate broad and narrow search terms with synonyms
- **🔥 NEW**: Review MIE files for database-specific performance requirements
- Test basic connectivity before complex queries

### Phase 2: Discovery (High Recall)
- Start with most permissive databases first (ChEBI, UniProt)
- Use graduated complexity: Simple queries → Complex joins
- Test query patterns before scaling up
- Have fallback strategies for strict databases

### Phase 3: Analysis (High Precision)
- **Follow MIE performance guidelines religiously**
- Use mandatory filters (ChEMBL: `standardType`, UniProt: `reviewed=1`)
- Keep result limits appropriate (ChEMBL: 15-25, others: 50-100)
- Break complex queries into components
- Test incrementally: Basic → Filters → Joins

### Phase 4: Cross-Database Integration
- Use persistent identifiers as integration keys
- Build cross-reference networks (TogoID works well)
- Harmonize data schemas and resolve semantic heterogeneity

### Phase 5: Validation and Enrichment
- Cross-validate annotations across sources
- Map to biological networks and pathways
- Prioritize high-quality evidence

---

## Database-Specific Patterns

### ChEMBL (Bioactivity)
```sparql
# ✅ MUST filter by standardType, limit < 30
SELECT ?molecule ?ic50 WHERE {
  ?activity cco:standardType "IC50" ;      # MANDATORY
            cco:standardValue ?ic50 ;
            cco:hasMolecule ?molecule .
  FILTER(?ic50 < 1000 && ?ic50 > 0)
} LIMIT 25
```

### UniProt (Proteins)
```sparql
# ✅ MUST filter by reviewed=1, limit < 100
SELECT ?protein ?name WHERE {
  ?protein up:reviewed 1 ;                # MANDATORY
           up:recommendedName ?nameObj .
  ?nameObj up:fullName ?name .
} LIMIT 50
```

### Reactome (Pathways)
```sparql
# ✅ MUST use STR() for string comparisons
SELECT ?pathway ?name WHERE {
  ?pathway bp:displayName ?name .
  FILTER(CONTAINS(LCASE(STR(?name)), "metabolism"))  # STR() required
}
```

---

## Critical Implementation Rules

### 🔥 **Database Documentation First**
- Read MIE files before any complex queries
- Identify mandatory filters and limits
- Test basic patterns before scaling

### ⚡ **Query Strategy**
1. **Start Simple**: `SELECT ?entity WHERE { ?entity a :Class } LIMIT 10`
2. **Add Gradually**: Properties → Filters → Joins
3. **Follow Database Rules**: Mandatory filters, appropriate limits
4. **Have Fallbacks**: API → Simple RDF → Complex RDF

### 🚨 **Performance Red Flags**
- **Immediate timeout**: Missing mandatory filters
- **Empty results**: Wrong syntax for database
- **Simple works, complex fails**: Need query decomposition

---

## Updated Pitfalls

### ❌ **New Database-Agnostic Mistakes**
- Ignoring MIE performance guidelines
- Using one-size-fits-all queries
- Skipping incremental testing
- Assuming query patterns transfer between databases

### ❌ **Classic Mistakes**
- Analysis-first: Starting with restrictive filters
- Discovery-only: Not validating results with structured queries
- Integration failures: Mixing different quality standards

---

## Quick Troubleshooting

**Query Failed?**
1. Check MIE requirements (filters, limits, syntax)
2. Simplify progressively 
3. Use database-specific patterns
4. Try fallback strategy

**Database-Specific Limits:**
- ChEMBL: Filter by `standardType`, limit 25
- UniProt: Filter by `reviewed=1`, limit 50
- Reactome: Use `STR()` for strings, limit 50

---

## Key Success Factors

✅ **Database Documentation**: MIE files are critical
✅ **Incremental Development**: Test simple before complex
✅ **Quality Filtering**: Use native quality indicators
✅ **Performance Monitoring**: Optimize based on response times

## Updated Takeaway
**Discover what's actually there, but respect each database's specific performance requirements and constraints.**

The methodology works excellently when properly implemented with database-specific optimizations.