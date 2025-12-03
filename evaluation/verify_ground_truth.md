# Ground Truth Verification Queries

Run each query to establish the current correct answer before validation.

## Q001: Reviewed human proteins
```sparql
PREFIX up: <http://purl.uniprot.org/core/>
SELECT (COUNT(DISTINCT ?protein) as ?count)
WHERE {
  ?protein a up:Protein ;
           up:reviewed 1 ;
           up:organism <http://purl.uniprot.org/taxonomy/9606> .
}
```
**Database:** uniprot
**Expected:** ~20,435 (may vary with releases)

---

## Q002: Approved drugs
```sparql
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT (COUNT(DISTINCT ?molecule) as ?count)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule a cco:SmallMolecule ;
            cco:highestDevelopmentPhase 4 .
}
```
**Database:** chembl
**Expected:** ~3,592

---

## Q003: Cryo-EM structures
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>
SELECT (COUNT(DISTINCT ?entry) as ?count)
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock ;
         pdbx:has_exptlCategory/pdbx:has_exptl ?exptl .
  ?exptl pdbx:exptl.method "ELECTRON MICROSCOPY" .
}
```
**Database:** pdb
**Expected:** ~15,032

---

## Q004: Human pathways in Reactome
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
SELECT (COUNT(DISTINCT ?pathway) as ?count)
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
           bp:organism ?organism .
  ?organism bp:name ?organismName .
  FILTER(STR(?organismName) = "Homo sapiens")
}
```
**Database:** reactome
**Expected:** ~2,673

---

## Q005: Best resolution structure
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?entry_id ?resolution
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_refineCategory/pdbx:has_refine ?refine .
  ?refine pdbx:refine.ls_d_res_high ?resolution .
  FILTER(xsd:decimal(?resolution) > 0)
}
ORDER BY xsd:decimal(?resolution)
LIMIT 5
```
**Database:** pdb
**Expected:** 0.48 Å (5D8V, 3NIR)

---

## Q006: Melanoma drugs
```sparql
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?label
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?drugInd cco:hasMolecule ?molecule ;
           cco:hasMeshHeading ?indication ;
           cco:highestDevelopmentPhase 4 .
  ?molecule rdfs:label ?label .
  FILTER(CONTAINS(LCASE(?indication), "melanoma"))
}
ORDER BY ?label
```
**Database:** chembl
**Expected:** 16 drugs

---

## Q007: GO kinase terms
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>
SELECT DISTINCT ?go ?label
WHERE {
  ?go rdfs:label ?label ;
      oboinowl:hasOBONamespace "molecular_function" .
  ?label bif:contains "'kinase'" .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
```
**Database:** go
**Expected:** 7 terms

---

## Q017: Imatinib approval status
```sparql
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label ?phase
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule rdfs:label ?label ;
            cco:highestDevelopmentPhase ?phase .
  ?label bif:contains "'imatinib'" .
}
```
**Database:** chembl
**Expected:** Phase 4

---

## Q021: p53 molecular weight
```sparql
PREFIX up: <http://purl.uniprot.org/core/>
SELECT ?mass
WHERE {
  ?protein up:mnemonic "P53_HUMAN" ;
           up:sequence ?seq .
  ?seq up:mass ?mass .
}
LIMIT 1
```
**Database:** uniprot
**Expected:** 43,653 Da

---

## Q027: Reactome organisms
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>
SELECT DISTINCT ?organismName (COUNT(DISTINCT ?pathway) as ?count)
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
           bp:organism ?organism .
  ?organism bp:name ?organismName .
}
GROUP BY ?organismName
ORDER BY DESC(?count)
```
**Database:** reactome
**Expected:** 15 organisms
