# ChEMBL RDF Schema Reference

## Overview
ChEMBL RDF provides semantic access to the ChEMBL database, which contains bioactivity data for chemical compounds and their biological targets. The RDF uses the namespace `http://rdf.ebi.ac.uk/terms/chembl#` for ChEMBL-specific terms.

## Core Classes

### Molecules
- **SmallMolecule**: Chemical compounds with molecular properties
- **Macromolecule**: Large molecules like proteins and nucleic acids  
- **Biological**: Biological compounds
- **Inorganic**: Inorganic chemical compounds
- **Metal**: Metal-containing compounds
- **NaturalProductDerived**: Compounds derived from natural products
- **Oligonucleotide**: Short nucleic acid sequences
- **Oligosaccharide**: Short carbohydrate chains

### Biotherapeutics
- **Antibody**: Antibody therapeutics
- **Mab**: Monoclonal antibodies
- **Fab**: Antibody fragments
- **ScFv**: Single-chain variable fragments
- **BiTE**: Bispecific T-cell engager
- **CellTherapy**: Cell-based therapeutics

### Targets
- **SingleProtein**: Individual protein targets
- **ProteinComplex**: Multi-protein complexes
- **ProteinComplexGroup**: Groups of related protein complexes
- **ProteinFamily**: Families of related proteins
- **ChimericProtein**: Engineered protein constructs
- **ProteinNucleicAcidComplex**: Protein-nucleic acid complexes
- **CellLine**: Cell line targets
- **CellLineTarget**: Cell line-based targets
- **SmallMoleculeTarget**: Small molecule targets
- **OligosaccharideTarget**: Carbohydrate targets

### Assays and Activities
- **Assay**: Bioassay experiments
- **Activity**: Measured biological activities
- **Mechanism**: Mechanism of action data

### Sources and References
- **Document**: Scientific publications
- **Journal**: Scientific journals
- **Source**: Data sources
- **Organism**: Taxonomic organisms

## Core Properties

### Identification
- **chemblId**: ChEMBL identifier (e.g., CHEMBL25)
- **label**: Human-readable label
- **prefLabel**: Preferred label

### Molecular Properties
- **atcClassification**: ATC therapeutic classification
- **moleculeProperties**: Chemical properties (MW, LogP, etc.)
- **canonicalSmiles**: SMILES representation
- **standardInchi**: InChI identifier
- **standardInchiKey**: InChI key

### Activity Data
- **standardType**: Measurement type (IC50, Ki, etc.)
- **standardValue**: Numerical value
- **standardUnits**: Units of measurement
- **standardRelation**: Relationship operator (=, >, <)
- **pChembl**: Negative log of molar activity

### Target Information
- **targetType**: Type of biological target
- **organismName**: Target organism
- **proteinSequence**: Protein sequence
- **taxonomy**: Taxonomic classification

### Assay Details
- **assayType**: Type of assay (Binding, Functional, etc.)
- **assayCategory**: Assay category
- **assayTestType**: Test methodology
- **assayTissue**: Tissue source
- **assayCellType**: Cell type used

## Relationship Properties

### Core Relationships
- **hasActivity**: Links molecules to their activities
- **hasAssay**: Links targets to assays
- **hasTarget**: Links assays to targets
- **hasMolecule**: Links activities to molecules
- **hasDocument**: Links to publication documents

### Cross-References
- **moleculeXref**: External molecule references
- **targetXref**: External target references
- **assayXref**: External assay references
- **xref**: Generic cross-references

### Hierarchical Relationships
- **hasParentMolecule**: Parent molecule relationship
- **hasChildMolecule**: Child molecule relationship
- **hasTargetComponent**: Target component relationships
- **hasProteinClassification**: Protein classification

### Ontology Links
- **hasMesh**: MeSH term associations
- **hasEFO**: Experimental Factor Ontology links
- **hasCLO**: Cell Line Ontology links
- **hasQUDT**: QUDT unit ontology links
- **hasUnitOnto**: Unit Ontology links

## External Database References

### Chemical Databases
- **ChebiRef**: ChEBI references
- **PubchemRef**: PubChem references
- **HmdbRef**: Human Metabolome Database
- **DrugbankDbRef**: DrugBank references

### Protein/Target Databases
- **UniprotRef**: UniProt references
- **EnsemblGeneRef**: Ensembl Gene references
- **PfamRef**: Pfam domain references
- **InterproRef**: InterPro references

### Pathway/Function Databases
- **GoComponentRef**: GO Cellular Component
- **GoFunctionRef**: GO Molecular Function
- **GoProcessRef**: GO Biological Process
- **ReactomeRef**: Reactome pathway references

### Structural Databases
- **ProteinDataBankRef**: PDB structure references

## Data Validation Properties

### Quality Indicators
- **dataValidityComment**: Data quality comments
- **dataValidityIssue**: Known data issues
- **potentialDuplicate**: Duplicate detection flag

### Publication Information
- **publishedType**: Original measurement type
- **publishedValue**: Original published value
- **publishedUnits**: Original units
- **publishedRelation**: Original relation

## Mechanism and Classification

### Drug Mechanisms
- **mechanismDescription**: Description of mechanism
- **mechanismActionType**: Type of action
- **isTargetForMechanism**: Target-mechanism links

### Classifications
- **fracClassification**: FRAC classification
- **hracClassification**: HRAC classification
- **iracClassification**: IRAC classification

## Usage Examples

### Find Activities for a Molecule
```sparql
PREFIX chembl: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?activity ?assay ?target ?type ?value ?units WHERE {
  ?molecule chembl:chemblId "CHEMBL25" ;
           chembl:hasActivity ?activity .
  ?activity chembl:hasAssay ?assay ;
           chembl:standardType ?type ;
           chembl:standardValue ?value ;
           chembl:standardUnits ?units .
  ?assay chembl:hasTarget ?target .
}
```

### Find Targets for a Compound Class
```sparql
PREFIX chembl: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT DISTINCT ?target ?targetName WHERE {
  ?molecule a chembl:SmallMolecule ;
           chembl:hasActivity ?activity .
  ?activity chembl:hasAssay ?assay .
  ?assay chembl:hasTarget ?target .
  ?target rdfs:label ?targetName .
}
```

### Query Bioactivity Data with Filters
```sparql
PREFIX chembl: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?molecule ?activity ?ic50 WHERE {
  ?molecule chembl:hasActivity ?activity .
  ?activity chembl:standardType "IC50" ;
           chembl:standardValue ?ic50 ;
           chembl:standardUnits "nM" .
  FILTER(?ic50 < 100)
}
```

## Common URI Patterns

- **Molecules**: `http://rdf.ebi.ac.uk/resource/chembl/molecule/{CHEMBL_ID}`
- **Activities**: `http://rdf.ebi.ac.uk/resource/chembl/activity/{CHEMBL_ACT_ID}`
- **Assays**: `http://rdf.ebi.ac.uk/resource/chembl/assay/{CHEMBL_ID}`
- **Targets**: `http://rdf.ebi.ac.uk/resource/chembl/target/{CHEMBL_ID}`
- **Documents**: `http://rdf.ebi.ac.uk/resource/chembl/document/{CHEMBL_ID}`

## Key Namespaces
- **chembl**: `http://rdf.ebi.ac.uk/terms/chembl#`
- **rdf**: `http://www.w3.org/1999/02/22-rdf-syntax-ns#`
- **rdfs**: `http://www.w3.org/2000/01/rdf-schema#`
- **skos**: `http://www.w3.org/2004/02/skos/core#`
- **dc**: `http://purl.org/dc/terms/`

This schema enables comprehensive queries across chemical structures, bioactivity data, targets, and associated metadata in the ChEMBL database.