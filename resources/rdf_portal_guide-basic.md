# RDF Portal Guide: Universal Workflow

## ⚠️ CRITICAL: Display vs Semantic Properties

**NEVER filter on display identifiers** (mnemonics, short names)  
**ALWAYS filter on semantic properties** (URIs, fullName, organism URIs)

**Priority order:**
1. Full URI: `VALUES ?protein { <http://purl.uniprot.org/uniprot/P05067> }`
2. Organism + fullName: `up:organism <.../9606> ; up:recommendedName/up:fullName "exact name"`
3. Descriptive filter: `FILTER(CONTAINS(LCASE(?fullName), "descriptive term"))`

---

## 4-STEP WORKFLOW
1. KEYWORD EXTRACTION
2. DATABASE SELECTION (two-tier: 3-5 core, 5-10 accessible)
3. INDIVIDUAL DATABASE QUERIES (ALL Tier 1 databases)
4. CROSS-DATABASE VALIDATION (≥50% of pairs)

---

## STEP 1: KEYWORD EXTRACTION

Extract 5-15 keywords by type: Proteins, Pathways, Diseases, Compounds, Other.

**📝 Create Artifact:** `rdf_analysis_results.md` with Step 1 results

---

## STEP 2: DATABASE SELECTION

### Core Principle: Quality Over Quantity
**Select 3-5 CORE databases (Tier 1) to query thoroughly.**  
**Access 5-10 SECONDARY databases (Tier 2) via cross-references.**

Run `list_databases()` to see all available databases.

### 2.1: Coverage Analysis (MANDATORY)

| Question Component | Data Type | Primary DBs | Secondary DBs | Score (1-5) |
|-------------------|-----------|-------------|---------------|-------------|
| [component] | [data?] | [will query] | [via cross-ref] | [score] |

**Scores:** 5=rich direct data, 4=good direct/cross-ref, 3=cross-ref only, 2=limited, 1=unavailable

### 2.2: Practical Constraints Check

- [ ] Can I query 3-5 databases thoroughly? (not 10+)
- [ ] 30-45 min per database for schema learning acceptable?
- [ ] Query performance issues? (ChEMBL, PubChem, DDBJ are large)
- [ ] Which databases are cross-reference hubs? (UniProt, Wikidata)
- [ ] Can I achieve 80% of goals with 3-4 databases?

### 2.3: Gaps & Strengths

```
GAPS: [Missing data] → [Impact]
MITIGATION: [Strategy or acknowledgment]
STRENGTHS: [What's well-covered]
```

### 2.4: Two-Tier Selection

#### TIER 1: Core (WILL QUERY - 3-5 databases)

| Database | Why Selected | Query Plan | Links To |
|----------|-------------|-----------|----------|
| db1 | [unique necessity] | [3-5 queries] | [Tier 2 DBs] |

**Criteria:** Necessity, Centrality, Coverage, Performance  
**CRITICAL:** Must query every Tier 1 database in Step 3

#### TIER 2: Accessible (VIA CROSS-REFS - 5-10 databases)

| Database | Via | Path | Data |
|----------|-----|------|------|
| PDB | UniProt | `rdfs:seeAlso` → "wwpdb" | structures |
| GO | UniProt | `up:classifiedWith` → "GO_" | annotations |

### 2.5: Self-Check (Answer All)

1. Can I actually query all Tier 1 databases? (if no → move to Tier 2)
2. Do I have 3-5 specific queries planned for each? (if no → remove)
3. Can I access Tier 2 via Tier 1 cross-refs? (if no → add to Tier 1 or gap)
4. Does each Tier 1 provide unique value? (if no → remove duplicate)
5. Am I being realistic? (if no → simplify)

**📝 Update Artifact:** Add Step 2 results

**Gate:** Coverage + constraints + both tiers + self-checks complete

---

## STEP 3: INDIVIDUAL DATABASE QUERIES

### Rules
- ✅ Query ALL Tier 1 (no exceptions)
- ✅ Actual SPARQL queries + results
- ✅ Capture exact URIs
- ✅ Document Tier 2 cross-ref access

### For EACH Tier 1 Database:

1. `get_MIE_file(dbname)` → read best_practices
2. Run 3-5 queries:

```
DATABASE: [name] (TIER 1)
QUERY: [purpose]
SPARQL: [code]
RESULTS: [data]
URIs: [captured]
CROSS-REFS: [to Tier 2]
```

### For EACH Tier 2 Database:

```
DATABASE: [name] (TIER 2)
VIA: [Tier 1 DB] → [property] → [filter]
EXAMPLE URI: [one found]
DATA: [what obtained]
```

### Source Tracking

```
FROM RDF (TIER 1): [Fact] - [DB + Query#]
FROM RDF (TIER 2): [Fact] - [DB1 → property → DB2]
FROM GENERAL KNOWLEDGE: [Fact] - [Why not RDF]
```

**Gate:** All Tier 1 queried, Tier 2 accessed, URIs captured, tracking complete

**📝 Update Artifact:** Add Step 3 results

---

## STEP 4: CROSS-DATABASE VALIDATION

### Rules
- ✅ Validate ≥50% of Tier 1 pairs
- ✅ Validate ≥3 Tier 1 ↔ Tier 2 connections
- ✅ Bidirectional (A→B AND B→A)
- ✅ Explicit RDF links only

### 4.1: Validation Matrix

For N Tier 1 DBs: N×(N-1)/2 pairs  
Mark: **Required** (critical) | **Optional** (nice) | **Skip** (no connection)  
Target: ALL Required + 25% Optional

### 4.2: For EACH Validation:

```
VALIDATION: [DB A] ↔ [DB B]
Entity: [what] | Importance: [why]

FORWARD: URI [A] → property → Found [B URI or NOT FOUND]
BACKWARD: URI [B] → property → Found [A URI or NOT FOUND]

RESULT: ✅ Bidirectional | ⚠️ Unidirectional | ❌ Failed
```

### 4.3: Summary Table

| Entity | DB1 | URI1 | DB2 | URI2 | Fwd | Rev | Status |
|--------|-----|------|-----|------|-----|-----|--------|
| X | db1 | uri1 | db2 | uri2 | ✅ | ✅ | VALIDATED |
| Y | db1 | uri3 | db4 | uri4 | ✅ | N/A | TIER 2 |

**Gate:** ≥50% Tier 1 pairs, ≥3 Tier 1↔2 links, all critical done, failures documented

**📝 Update Artifact:** Add Step 4 results

---

## COMPLETION CHECKLIST

**Step 1:** [ ] 5-15 keywords by type

**Step 2:** [ ] Coverage with tiers | [ ] Constraints assessed | [ ] Tier 1: 3-5 DBs | [ ] Tier 2: 5-10 DBs | [ ] Self-checks done

**Step 3:** [ ] ALL Tier 1 queried | [ ] Tier 2 accessed | [ ] URIs captured | [ ] Sources tracked

**Step 4:** [ ] ≥50% Tier 1 pairs | [ ] ≥3 Tier 1↔2 links | [ ] Summary table

**Quality:** [ ] One finding | [ ] One limitation | [ ] Validated vs assumed clear

---

## RED FLAGS

**Stop if:** "Sounds relevant" | "Y cross-refs it" | "Might need later" | "8+ databases" | "Can't plan queries" | "Obviously links" | "I know it's true"

**Good if:** 3-5 Tier 1 | Query plans ready | Cross-ref paths documented | Unique value | Realistic scope

---

## QUALITY GATES

**2→3:** Tiers complete + constraints + self-checks + no red flags  
**3→4:** ALL Tier 1 queried + Tier 2 accessed + URIs + tracking  
**4→Done:** ≥50% validated + table + failures explained

---

## KEY PRINCIPLES

**Quality > Quantity:** Better 3 deep + 7 cross-refs than 10 superficial

**Honest Labels:** RDF data | Tier 2 cross-ref | General knowledge | Gap

**Cross-Ref Power:** Access 10-15 databases by querying 3-5 (efficient, not lazy)

**Validation Required:** Even Tier 2 needs validation with example URIs

---

## EXAMPLE

❌ **Poor:** 10 Tier 1 databases, no cross-refs, vague plans  
✅ **Good:** 3 Tier 1 (UniProt, Reactome, ChEMBL) + 5 Tier 2 (PDB, GO, ChEBI, MeSH, Taxonomy via cross-refs)

**Common patterns:**
- **Protein:** UniProt + Reactome + ChEMBL → access PDB, GO, ChEBI, Taxonomy
- **Disease:** UniProt + MeSH/Mondo + Reactome → access ChEMBL, Wikidata, PubChem
- **Drug:** ChEMBL + UniProt + ChEBI → access Reactome, GO, PDB, MeSH