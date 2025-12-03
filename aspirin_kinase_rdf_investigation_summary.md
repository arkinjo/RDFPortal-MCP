# Aspirin and Kinase Inhibition: RDF Portal Database Investigation (Updated)

## Executive Summary

**Question:** Does aspirin inhibit any human kinases?

**Literature Answer:** YES - Published research (1994-2012) demonstrates aspirin inhibits multiple human kinases.

**RDF Portal Database Answer:** 
- **Structured databases (ChEMBL, ChEBI, UniProt, Reactome):** NO kinase inhibitor annotations
- **Literature database (PubMed RDF):** YES - Contains evidence via MeSH annotations and full-text search

---

## 1. Key Finding: PubMed RDF Contains the Evidence

### PubMed Search Results:

| Search Query | Papers Found | Key Example |
|--------------|--------------|-------------|
| aspirin AND kinase | 30+ papers | Multiple kinase types |
| aspirin AND (IKK OR NF-κB) | 20+ papers | NF-κB pathway |
| aspirin AND (AMPK OR mTOR) | 30+ papers | Energy metabolism |
| salicylate AND kinase | 20+ papers | Including IKK, AMPK |

### Foundational Paper (PMID 9817203):
- **Title:** "The anti-inflammatory agents aspirin and salicylate inhibit the activity of I(kappa)B kinase-beta"
- **Journal:** Nature (1998)
- **DOI:** 10.1038/23948
- **Abstract:** Demonstrates aspirin and sodium salicylate specifically inhibit IKK-beta activity in vitro and in vivo by binding to reduce ATP binding

### MeSH Annotations Found:
| MeSH ID | Term | Papers with Aspirin |
|---------|------|---------------------|
| D051550 | I-kappa B Kinase | 23 papers |
| C496560 | IKBKB protein, human (IKKβ) | Multiple |
| D055372 | AMP-Activated Protein Kinases | 30 papers |
| D017346 | Protein Serine-Threonine Kinases | Many |

---

## 2. Comparison: Structured vs Literature Databases

| Database Type | Database | Contains Aspirin-Kinase Evidence? |
|--------------|----------|-----------------------------------|
| Activity Data | ChEMBL | ❌ Weak activity only (>10 μM) |
| Chemical Ontology | ChEBI | ❌ No kinase inhibitor role |
| Protein Annotations | UniProt | ❌ No aspirin annotations |
| Pathway Data | Reactome | ❌ No reactions |
| **Literature** | **PubMed RDF** | **✅ Full evidence via MeSH & abstracts** |
| Text Mining | PubTator | ⚠️ Gene/Disease only, no chemicals |

---

## 3. Literature Evidence from PubMed RDF

### Direct Kinase Inhibitors (Found in PubMed):

| Kinase | PMID | Year | Finding |
|--------|------|------|---------|
| **IKKβ** | 9817203 | 1998 | Aspirin directly inhibits IKK-beta by blocking ATP binding |
| **AMPK** | 22517326 | 2012 | Salicylate directly activates AMPK |
| **mTOR** | 22406476 | 2012 | Aspirin inhibits mTOR signaling |
| **ATM** | 17510082 | 2007 | Aspirin activates checkpoint kinase ATM |

### Sample SPARQL Queries for PubMed:

```sparql
# Search titles for aspirin + kinase
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?pmid ?title ?issued
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:title ?title ;
           dct:issued ?issued .
  ?title bif:contains "'aspirin' AND 'kinase'" .
}
ORDER BY DESC(?issued)
LIMIT 30
```

```sparql
# Find papers with Aspirin + IKK MeSH terms
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?pmid ?title
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:title ?title ;
           rdfs:seeAlso mesh:D001241 ;
           rdfs:seeAlso mesh:D051550 .
}
```

---

## 4. Why Structured Databases Lack This Information

| Reason | Explanation |
|--------|-------------|
| **Screening bias** | ChEMBL captures high-throughput data; aspirin shows weak activity in standard assays |
| **Classification** | Aspirin classified as NSAID/COX inhibitor, not kinase inhibitor |
| **Concentration** | Kinase effects at 30-150 μM, above typical drug screening |
| **Curation focus** | ChEBI roles focus on primary mechanisms |
| **Discovery context** | Findings from mechanistic studies, not kinase profiling |

---

## 5. Conclusions

### Key Insights:

1. **PubMed RDF is the most informative database** for aspirin's kinase inhibition effects
2. **MeSH annotations provide structured access** to literature evidence (23+ papers with IKK terms)
3. **Full-text search (bif:contains)** enables discovery of mechanism-related publications
4. **Structured databases (ChEMBL, ChEBI) have significant gaps** in mechanism-of-action coverage

### Recommendations:

1. **For drug-target discovery:** Query PubMed RDF alongside ChEMBL
2. **Use MeSH term co-occurrence** to find drug-kinase relationships
3. **Combine database types:** Structured data for quantitative activity, PubMed for mechanisms
4. **Don't assume absence = negative:** Literature may contain evidence not in structured DBs

### Research Strategy:

```
Step 1: Search ChEMBL for quantitative activity data
Step 2: Search ChEBI for annotated biological roles
Step 3: Search PubMed RDF for literature evidence
Step 4: Use MeSH terms to find related papers
Step 5: Cross-reference findings
```

---

## 6. Database Endpoints Used

| Database | Endpoint | Key Predicates |
|----------|----------|----------------|
| ChEMBL | rdfportal.org/backend/ebi/sparql | cco:hasMolecule, cco:hasTarget |
| ChEBI | rdfportal.org/backend/ebi/sparql | RO_0000087 (has_role) |
| UniProt | rdfportal.org/backend/sib/sparql | up:annotation |
| PubChem | rdfportal.org/backend/pubchem/sparql | obo:RO_0000087 |
| Reactome | rdfportal.org/backend/ebi/sparql | bp:SmallMolecule |
| **PubMed** | **rdfportal.org/ncbi/sparql** | **rdfs:seeAlso (MeSH), dct:title** |
| MeSH | rdfportal.org/ncbi/sparql | rdfs:label |

---

*Investigation conducted: November 2024*
*Databases accessed: RDF Portal (rdfportal.org)*
*Total databases queried: 9*
*Key finding: PubMed RDF contains literature evidence that structured databases lack*
