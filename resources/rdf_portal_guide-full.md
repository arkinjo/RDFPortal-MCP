# RDF Portal Guide: Universal Workflow

## ⚠️ CRITICAL: Query by Semantics, Not Display Names

**NEVER** filter on mnemonics/short names. **ALWAYS** use:
1. Full URI: `VALUES ?protein { <http://purl.uniprot.org/uniprot/P05067> }`
2. Organism + fullName: `up:organism <.../9606> ; up:recommendedName/up:fullName "exact name"`
3. Descriptive: `FILTER(CONTAINS(LCASE(?fullName), "term"))`

---

## 4-STEP WORKFLOW
1. KEYWORD EXTRACTION & STANDARDIZATION
2. DATABASE SELECTION (3-5 core + 5-10 via cross-refs)
3. QUERIES (API → SPARQL)
4. VALIDATION (TogoID → SPARQL fallback)

---

## STEP 1: KEYWORDS & STANDARDIZATION

### 1.1: Extract 5-15 Keywords FROM QUERY ONLY
**⚠️ CRITICAL:** Extract keywords ONLY from the user's query. Do NOT add terms from domain knowledge.

Categorize: Proteins, Pathways, Diseases, Compounds, Other

### 1.2: OLS Standardization
For each keyword:
1. `search_terms(query="keyword", rows=5)`
2. Select best match (check ontology, label, definition)
3. `get_term_info(id="...")` for details

**Document:**
| Original | Type | OLS Term | Ontology:ID | Label | Status |
|----------|------|----------|-------------|-------|--------|
| cancer | Disease | MONDO:0004992 | MONDO | cancer | ✅ |
| my-prot | Protein | - | - | - | ⚠️ |

**Status:** ✅ Found | ⚠️ No match (use original) | 🔄 Updated term

**📝 Artifact:** `rdf_analysis_results.md` with keywords table

---

## STEP 2: DATABASE SELECTION

### Core Principle: 3-5 CORE (Tier 1) + 5-10 VIA CROSS-REFS (Tier 2)

Run `list_database()` to see all available databases.

### 2.1: Coverage Analysis

| Component | Data Type | Tier 1 DBs | Tier 2 DBs | Score |
|-----------|-----------|------------|------------|-------|
| [what] | [type] | [query] | [cross-ref] | 1-5 |

**Score:** 5=rich direct, 4=good, 3=cross-ref only, 2=limited, 1=none

### 2.2: Constraints Check
- [ ] Can query 3-5 databases thoroughly?
- [ ] Query performance OK? (ChEMBL/PubChem/DDBJ are large)
- [ ] Cross-ref hubs identified? (UniProt, Wikidata)
- [ ] 80% goals achievable with 3-4 DBs?

### 2.3: Two-Tier Selection

**TIER 1 (WILL QUERY):**
| Database | Why | Query Plan | Links To |
|----------|-----|------------|----------|
| db1 | necessity | 3-5 queries | Tier 2 DBs |

**TIER 2 (VIA CROSS-REFS):**
| Database | Via | Path | Data |
|----------|-----|------|------|
| PDB | UniProt | `rdfs:seeAlso` → "wwpdb" | structures |

### 2.4: Self-Check
1. Can I query ALL Tier 1? (no → move to Tier 2)
2. 3-5 queries planned per Tier 1? (no → remove)
3. Tier 2 accessible via Tier 1? (no → add to Tier 1 or gap)
4. Each Tier 1 unique? (no → remove)
5. Realistic? (no → simplify)

**Gate:** Coverage + constraints + tiers + self-checks complete

**📝 Update Artifact:** Add Step 2

---

## STEP 3: QUERIES

### Rules: API → SPARQL → Document All

### 3.1: For EACH Tier 1 Database

**A. API Search (if available):**
- UniProt: `search_uniprot_entity()`
- ChEMBL: `search_chembl_target/molecule()`
- PubChem: `get_pubchem_compound_id()`
- PDB: `search_pdb_entity()`
- MeSH: `search_mesh_entity()`
- Wikidata: `search_wikidata_entity()`

**Document:**
```
DB: [name] | API: [tool] | Keywords: [searched]
Results: [Name] | ID: [id] | URI: [uri]
Status: ✅ [n] found | ⚠️ No API | ❌ No match
```

**B. SPARQL Details:**
1. `get_MIE_file(dbname)` for schema
2. Run 3-5 queries (use API IDs/URIs when available)

```
DB: [name] | Query #[n]: [purpose]
Target: [from API or exploratory]
SPARQL: [code]
Results: [data] | URIs: [captured] | Cross-refs: [to Tier 2]
```

### 3.2: For EACH Tier 2 Database

```
DB: [name] (TIER 2)
Via: [Tier 1] → [property] → [filter]
Example: [URI] | Data: [obtained]
```

### Source Tracking
- **API:** [fact] - [tool + DB]
- **RDF Tier 1:** [fact] - [DB + Query#]
- **RDF Tier 2:** [fact] - [DB1 → property → DB2]
- **Knowledge:** [fact] - [why not RDF]

**Gate:** All Tier 1 queried, Tier 2 accessed, URIs captured

**📝 Update Artifact:** Add Step 3

---

## STEP 4: VALIDATION

### Rules: TogoID First → SPARQL Only if Needed

### 4.1: Validation Matrix
For N Tier 1 DBs: N×(N-1)/2 pairs  
Mark: **Required** | **Optional** | **Skip**  
Target: ALL Required + 25% Optional

### 4.2: Two-Stage Validation

**Stage 1: TogoID (PRIMARY)**
```
1. getRelation(source="db1", target="db2")
   → No result? Go to Stage 2

2. Forward: convertId(ids="id1,id2", route="db1,db2", report="pair")
3. Backward: convertId(ids="...", route="db2,db1", report="pair")

Document:
DB A ↔ DB B (TogoID) | IDs: [...] | Datasets: [a,b]
Forward: [n] conversions | Backward: [n] conversions
Result: ✅ Bidirectional | ⚠️ Uni | ❌ Failed
```

**Stage 2: SPARQL (FALLBACK)**
```
DB A ↔ DB B (SPARQL) | Reason: [why not TogoID]
Forward: URI [A] → property → [B or NOT FOUND]
Backward: URI [B] → property → [A or NOT FOUND]
Result: ✅ Bidirectional | ⚠️ Uni | ❌ Failed
```

### 4.3: Summary

| Entity | DB1 | ID1 | DB2 | ID2 | Fwd | Rev | Method | Status |
|--------|-----|-----|-----|-----|-----|-----|--------|--------|
| X | uniprot | P05067 | pdb | 1AAP | ✅ | ✅ | TogoID | ✅ |

**Gate:** ≥50% Tier 1 pairs, ≥3 Tier 1↔2, TogoID first, failures explained

**📝 Update Artifact:** Add Step 4

---

## CHECKLIST

- **Step 1:** [ ] Keywords | [ ] OLS done | [ ] Table
- **Step 2:** [ ] Coverage | [ ] Constraints | [ ] Tier 1: 3-5 | [ ] Tier 2: 5-10 | [ ] Self-check
- **Step 3:** [ ] API used | [ ] All Tier 1 | [ ] Tier 2 accessed | [ ] URIs | [ ] Tracked
- **Step 4:** [ ] ≥50% pairs | [ ] ≥3 Tier1↔2 | [ ] TogoID first | [ ] Table
- **Quality:** [ ] Finding | [ ] Limitation | [ ] Validated vs assumed

---

## GATES

- **1→2:** Keywords extracted + OLS standardized
- **2→3:** Tiers + constraints + self-checks + no red flags
- **3→4:** API used + All Tier 1 queried + Tier 2 accessed + URIs
- **4→Done:** ≥50% validated + TogoID first + table + failures

---

## KEY PRINCIPLES

- **Quality > Quantity:** 3 deep + 7 cross-refs beats 10 superficial
- **API → SPARQL:** Identify entries with APIs, detail with SPARQL
- **TogoID → SPARQL:** Validate with TogoID first, SPARQL only if needed
- **Cross-Ref Power:** Query 3-5, access 10-15 (efficient design)
- **Honest Labels:** API | RDF Tier 1 | RDF Tier 2 | Knowledge | Gap

---

## RED FLAGS vs GOOD SIGNS

**🛑 Stop if:** "Sounds relevant" | "Might need later" | 8+ databases | No query plans | "Obviously links"

**✅ Good if:** 3-5 Tier 1 | Query plans ready | Cross-ref paths | Unique value | Realistic

---

## EXAMPLES

**Common Patterns:**
- **Protein:** UniProt + Reactome + ChEMBL → PDB, GO, ChEBI, Taxonomy
- **Disease:** UniProt + MeSH/Mondo + Reactome → ChEMBL, Wikidata, PubChem
- **Drug:** ChEMBL + UniProt + ChEBI → Reactome, GO, PDB, MeSH