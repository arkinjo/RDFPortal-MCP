# Create a compact yet comprehensive MIE file for __DBNAME__ RDF database.

## Philosophy: Essential over Exhaustive
Create documentation that is **compact, clear, and complete** - sufficient for researchers to effectively query the database without unnecessary bloat.

## 1. Discovery Phase
- Use `get_sparql_endpoints()` to identify available endpoints
- Use `get_graph_list(dbname)` to find relevant named graphs
- Call `rdf_portal_guide()` for the general instructions on SPARQL queries
- Attempt `get_shex(dbname)` to retrieve existing shape expressions
- Attempt `get_MIE_file(dbname)` to retrieve existing MIE files
- Run exploratory SPARQL queries using `run_sparql(dbname, sparql_query)` to understand the data structure

## 2. Schema Analysis
- Query for all RDF classes and their labels
- Query for all properties and their types (ObjectProperty, DatatypeProperty, etc.)
- Identify the most frequent entity types and their counts
- Examine sample instances to understand property usage patterns

## 3. Deep Dive Investigation
- Select representative entities and examine all their properties
- Map relationships between different entity types
- Identify cross-reference patterns to external databases
- Understand hierarchical or taxonomic structures if present

## 4. Shape Expression Creation (Efficiency Guidelines)
- If ShEx is available, include all the ShEx components in the shape_expressions section
- If no ShEx exists, reverse-engineer shape expressions from the data
- Define required vs optional properties based on actual data patterns
- Include appropriate data types and value constraints

**Commenting Guidelines:**
- **DO**: Comment non-obvious properties, complex patterns, or data type quirks
- **DON'T**: Comment every property with redundant information
- **DON'T**: Write comments like "# Unique identifier" for obviously named properties
- **DO**: Keep comments concise (one line maximum)
- **Example of good commenting:**
  ```
  schema:hasTaxID . ;                           # Mixed types (integer/string)
  schema:hasReference @<ReferenceShape> ;
  schema:isTypeStrain xsd:boolean ;
  ```

## 5. Validation & Documentation

### Sample RDF Entries (Target: Exactly 5 examples)
Select 5 diverse examples covering these categories (one example per category):
1. **Core Entity**: Main entity type with key properties
2. **Related Entity**: Secondary entity showing relationships
3. **Sequence/Molecular Data**: If applicable (genetic, protein, chemical data)
4. **Cross-reference**: Entity showing external database links
5. **Geographic/Temporal**: If applicable (location, time-series, metadata)

**Example Selection Criteria:**
- Use real data from the database
- Show different property patterns
- Demonstrate key relationships
- Keep descriptions concise (1-2 sentences)

### SPARQL Query Examples (Target: Exactly 7 queries)
Create 7 queries with this distribution:
- **2 basic**: Simple retrieval, filtering (e.g., get entities by type, basic property filtering)
- **3 intermediate**: Aggregation, grouping, moderate filtering (e.g., count by category, find entities in range)
- **2 advanced**: Complex joins, multiple patterns, nested queries (e.g., multi-entity integration, federated patterns)

**Query Categories to Cover** (select 7 from these):
1. Taxonomic/hierarchical retrieval
2. Phenotypic/characteristic filtering
3. Sequence data integration
4. External cross-references
5. Geographic distribution
6. Aggregation/statistics
7. Multi-entity complex integration

**For Each Query Include:**
- Descriptive title
- Concise description (1-2 sentences)
- Natural language question
- Complexity level (basic/intermediate/advanced)
- **Tested and working** SPARQL query

### Cross-references (Target: Comprehensive coverage by pattern)
Document **all external database cross-references** by organizing them into RDF patterns. Group databases that share the same RDF relationship pattern together. Include:
- **The RDF pattern** (e.g., rdfs:seeAlso, up:classifiedWith, up:organism)
- **List of databases** using that pattern, organized by category
- **Coverage information** for major databases where relevant
- **One representative SPARQL query** demonstrating the pattern

**For Each Pattern Group:**
- Show the common RDF property/relationship
- List all databases following this pattern, grouped by purpose
- Provide one working SPARQL example that can be adapted for any database in the group
- Include notes on filtering by URL pattern to distinguish databases
- Keep descriptions concise

## 6. Architectural Notes (Use Structured YAML Format)
Organize into exactly 4 categories with concise bullet points:

```yaml
architectural_notes:
  schema_design:
    - Key entity relationships and patterns
    - Central hub entities
    - Reference/citation systems
  
  performance:
    - Which queries are optimized
    - Index-friendly patterns
    - Query optimization tips
  
  data_integration:
    - External database mappings
    - Cross-reference patterns
    - Integration points
  
  data_quality:
    - Known data type issues
    - Missing data patterns
    - Validation notes
```

**Guidelines:**
- Use bullet points, NOT prose paragraphs
- Keep each bullet to one line when possible
- Focus on practical query-writing information
- No markdown headers or formatting within this section

## 7. Data Statistics

Create a data_statistics section that helps users write efficient queries and set realistic expectations. Invest approximately **5-10 minutes** gathering these statistics.

### Required Statistics Categories:

**A. Entity Counts** (Always include - 1 minute)
- Total counts for each major entity type (e.g., compounds, proteins, assays)
- Counts for important subsets (e.g., FDA-approved drugs, human proteins)
- Format: `total_<entity_type>: <count>`

**Example queries:**
```sparql
SELECT (COUNT(?s) as ?count) WHERE { ?s a <EntityType> }
```

**B. Data Coverage** (Critical for query planning - 3-4 minutes)

Measure what percentage of entities have key properties. This tells users which properties are reliable for filtering vs optional.

**How to gather:**
- Use sampling for large datasets (LIMIT 1000-10000 entities)
- Test 5-10 most important properties
- Express as ranges: "~95%", ">99%", "<5%", "~50%"

**Sampling query pattern:**
```sparql
# Sample approach for coverage
SELECT (COUNT(?prop) as ?withProp) WHERE {
  { SELECT ?entity WHERE { ?entity a <EntityType> } LIMIT 1000 }
  ?entity <property> ?prop .
}
# Calculate: (withProp / 1000) * 100 = coverage %
```

**What to test:**
- Essential descriptors (e.g., labels, identifiers)
- Key scientific properties (e.g., sequences, molecular weights)
- External database links (e.g., UniProt, Wikidata, PDB)
- Important annotations (e.g., classifications, roles)

**Format:**
```yaml
coverage:
  <entities>_with_<property>: "~XX%"
  compounds_with_labels: ">99%"
  compounds_with_wikidata_links: "~2%"
  proteins_with_sequences: ">99%"
  proteins_with_pdb_structures: "~60%"
```

**C. Property Cardinality** (Prevents result explosion - 2-3 minutes)

For one-to-many relationships, provide average and maximum counts. This warns users about properties that multiply result rows.

**Test with queries like:**
```sparql
SELECT (AVG(?count) as ?avgCount) (MAX(?count) as ?maxCount) WHERE {
  {
    SELECT ?entity (COUNT(?related) as ?count) WHERE {
      ?entity <relationship> ?related .
    } GROUP BY ?entity
    LIMIT 10000
  }
}
```

**What to test:**
- Relationships that commonly appear in joins (e.g., stereoisomers, isoforms)
- Cross-references to other databases
- Multi-valued properties (e.g., synonyms, publications)

**Format:**
```yaml
cardinality:
  avg_<related>_per_<entity>: X.X
  max_<related>_per_<entity>: XXXX
  avg_stereoisomers_per_compound: 2.3
  max_stereoisomers_per_compound: 740
  avg_pdb_structures_per_protein: 4.2
```

**D. Query Performance Patterns** (From empirical testing - collect during query development)

Document performance characteristics discovered while testing SPARQL queries:
- Which query patterns timeout or are slow
- Which properties work well for filtering
- Efficient vs inefficient join patterns
- Recommended LIMIT sizes for different query types
- Any quirks about text search, REGEX, or FILTER performance

**Format:**
```yaml
performance_characteristics:
  - "Property X is efficient for filtering up to Y results"
  - "Label REGEX searches timeout without specific ID filtering"
  - "Recommend LIMIT <N> for query type Y"
  - "Cross-graph joins between X and Y are optimized"
  - "Aggregation queries with GROUP BY work well for <condition>"
```

**E. Data Quality Summary** (Key points only - already mostly in architectural_notes)

Brief notes on:
- Data type inconsistencies (e.g., "property X has mixed types")
- Common completeness issues (e.g., "~Y% missing property Z")
- Known edge cases or special handling needed

### Template Structure:

```yaml
data_statistics:
  # A. Entity Counts (required)
  total_<entity_type>: <count>
  <subset>_<entity_type>: <count>
  
  # B. Data Coverage (required - use sampling)
  coverage:
    <entities>_with_<property>: "~XX%"
    <entities>_with_<key_descriptor>: ">YY%"
    <entities>_with_<external_link>: "<ZZ%"
    
  # C. Property Cardinality (required for one-to-many)
  cardinality:
    avg_<related>_per_<entity>: X.X
    max_<related>_per_<entity>: XXXX
    
  # D. Query Performance (from testing - highly valuable)
  performance_characteristics:
    - "Specific performance observation from query testing"
    - "Another pattern discovered during development"
    
  # E. Data Quality (key points only)
  data_quality_notes:
    - "Brief note on data type issue"
    - "Completeness observation"
```

### Implementation Guidelines:

1. **For Entity Counts**: Run simple COUNT queries for each major type

2. **For Coverage Statistics**:
   - Use sampling (LIMIT 1000-10000) for expensive queries
   - Test 5-10 most important properties
   - Express as ranges ("~95%", "<5%", ">99%")
   - Focus on properties users will query on

3. **For Cardinality**:
   - Test 3-5 important one-to-many relationships
   - Include both AVG and MAX
   - Use LIMIT in subqueries to avoid timeouts

4. **For Performance Patterns**:
   - Document findings from SPARQL query testing
   - Note which example queries worked vs timed out
   - Include practical recommendations based on experience

5. **Time Management**:
   - Spend ~5-10 minutes total on statistics
   - Use sampling to keep queries fast
   - Document "estimate" or "sample-based" if needed
   - Skip statistics that take >2 minutes to compute

### Statistics to AVOID:

- ❌ Overly detailed breakdowns (counts per year, per source, etc.)
- ❌ Statistics requiring complex computation (>2 min to gather)
- ❌ Redundant information already in shape expressions
- ❌ Internal implementation details not relevant to users
- ❌ Exact percentages when estimates suffice

### Quality Checklist:
- [ ] Entity counts for all major types
- [ ] Coverage estimates for 5-10 key properties (using sampling)
- [ ] Cardinality (avg/max) for 3-5 one-to-many relationships
- [ ] Performance notes from actual query testing
- [ ] All statistics gathered in reasonable time (~5-10 min)
- [ ] Statistics are actionable for query writing
- [ ] Used sampling for expensive queries

### Example: Good Statistics Section

```yaml
data_statistics:
  # Entity counts
  total_compounds: 119093251
  total_proteins: 248623
  fda_approved_drugs: 17367
  
  # Coverage (sampled from 10K entities)
  coverage:
    compounds_with_labels: ">99%"
    compounds_with_molecular_weight: "~98%"
    compounds_with_smiles: "~95%"
    compounds_with_wikidata_links: "~2%"
    compounds_with_chebi_classification: "~5%"
    proteins_with_sequences: ">99%"
    proteins_with_pdb_structures: "~60%"
  
  # Cardinality
  cardinality:
    avg_stereoisomers_per_compound: 2.3
    max_stereoisomers_per_compound: 740
    avg_descriptors_per_compound: 25
    avg_pdb_structures_per_protein: 4.2
    max_pdb_structures_per_protein: 1196
  
  # Performance (from testing)
  performance_characteristics:
    - "Label REGEX searches timeout without CID filtering"
    - "Molecular weight range queries efficient up to 10K results"
    - "Cross-graph compound+descriptor joins are optimized"
    - "Recommend LIMIT 100 for exploratory queries"
    - "Stereoisomer queries can return many rows per compound"
  
  # Data quality
  data_quality_notes:
    - "Descriptor values use mixed types (string/decimal/integer)"
    - "Not all compounds have complete descriptor sets"
    - "External links vary in completeness (2-95% coverage)"
```

## 8. MIE File Generation
- Create a complete YAML-formatted MIE file with proper structure
- Follow the target numbers: 5 RDF examples, 7 SPARQL queries, comprehensive pattern-based cross-references
- Use structured YAML for architectural_notes (not prose)
- Verify all SPARQL queries return results before inclusion
- Gather data_statistics using sampling when needed
- Organize cross-references by RDF pattern for compactness
- Check compliance with the MIE File Structure Template below
- Save the file using `save_MIE_file`

## Key Requirements
- Focus on **biological relevance**
- Ensure all examples use **real data** from the database
- **Prioritize compactness**: Essential over exhaustive
- Test and validate all SPARQL queries before inclusion
- Use **sampling** for expensive statistics
- Make documentation **immediately useful** for query writing

## Efficiency Checklist Before Saving
- [ ] ShEx has minimal redundant comments (only non-obvious properties commented)
- [ ] Exactly 5 diverse RDF examples (not 6, not 8)
- [ ] Exactly 7 SPARQL queries covering different complexity levels
- [ ] Comprehensive cross-references organized by RDF pattern with all databases listed
- [ ] Architectural notes in structured YAML format (no prose paragraphs)
- [ ] Data statistics with coverage, cardinality, and performance notes
- [ ] Used sampling for expensive statistics (kept under 10 minutes total)
- [ ] All descriptions are concise (1-2 sentences)
- [ ] All SPARQL queries have been tested and work

## Available Tools
- `get_sparql_endpoints()` - Get available SPARQL endpoints
- `get_graph_list(dbname)` - List named graphs in database
- `run_sparql(dbname, sparql_query)` - Execute SPARQL queries
- `get_shex(dbname)` - Retrieve ShEx schema if available
- `get_MIE_file(dbname)` - Retrieve existing MIE file if available
- `save_MIE_file(dbname, mie_content)` - Save the final MIE file

## MIE File Structure Template
```yaml
schema_info:
  title: [DATABASE_NAME]
  description: |
    [Comprehensive but concise description - 3-5 sentences covering:
     - What the database contains
     - Main entity types
     - Primary use cases
     - Key features]
  endpoint: https://rdfportal.org/primary # Replace with actual endpoint
  base_uri: http://example.org/ # Replace with actual base URI
  graphs: # List of named graphs
    - http://example.org/dataset

shape_expressions: |
  # Reverse-engineered from actual data
  # Include all standard and database-specific PREFIXes
  # Comment only non-obvious properties or complex patterns
  # Adhere to ShExC (ShEx Compact) syntax
  
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  
  <EntityShape> {
    a [ schema:EntityType ] ;
    rdfs:label xsd:string ;
    schema:property xsd:string ;           # Only comment when needed
    schema:complexProperty @<OtherShape>   # Relationships
  }

sample_rdf_entries:
  # Exactly 5 diverse examples (one per category)
  - title: [Descriptive title]
    description: [Concise 1-2 sentence description]
    rdf: |
      # Real RDF instance from database
  
  - title: [Another example]
    description: [Brief description]
    rdf: |
      # Real RDF instance

sparql_query_examples:
  # Exactly 7 queries: 2 basic, 3 intermediate, 2 advanced
  - title: [Descriptive title]
    description: [Concise 1-2 sentence description]
    question: [Natural language question this query answers]
    complexity: basic  # or intermediate, or advanced
    sparql: |
      PREFIX schema: <http://example.org/schema/>
      SELECT ?s ?p ?o
      FROM <http://example.org/dataset>
      WHERE { 
        ?s ?p ?o .
      }
      LIMIT 10

cross_references:
  # Pattern-based organization of cross-references
  - pattern: rdfs:seeAlso
    description: |
      Most external database links use rdfs:seeAlso property.
      Databases distinguished by URL patterns in the IRI.
    databases:
      sequence:
        - EMBL (embl/): ~95% coverage
        - RefSeq (refseq/): ~80% coverage
      structure:
        - PDB (wwpdb.org): ~25% coverage
        - AlphaFold (alphafolddb/): >98% coverage
        - SWISS-MODEL (smr/): ~40% coverage
      identifiers:
        - HGNC (hgnc/): 100% human
        - neXtProt (nextprot.org): 100% human
        - Gene IDs (geneid/): ~90% coverage
      # ... list other categories
    complexity: basic
    sparql: |
      PREFIX up: <http://purl.uniprot.org/core/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?protein ?mnemonic ?externalDB
      WHERE {
        ?protein a up:Protein ;
                 up:mnemonic ?mnemonic ;
                 up:reviewed 1 ;
                 rdfs:seeAlso ?externalDB .
        # Filter by URL pattern for specific database:
        # FILTER(CONTAINS(STR(?externalDB), "rdf.wwpdb.org")) # PDB
        # FILTER(CONTAINS(STR(?externalDB), "alphafolddb")) # AlphaFold
        # FILTER(CONTAINS(STR(?externalDB), "purl.uniprot.org/hgnc/")) # HGNC
      }
      LIMIT 30
  
  - pattern: up:classifiedWith
    description: Ontology classifications via up:classifiedWith property
    databases:
      - Gene Ontology (GO_): >85% coverage
      - Other classification systems
    complexity: basic
    sparql: |
      PREFIX up: <http://purl.uniprot.org/core/>
      SELECT ?protein ?classification
      WHERE {
        ?protein a up:Protein ;
                 up:reviewed 1 ;
                 up:classifiedWith ?classification .
        # Filter for specific ontology:
        # FILTER(STRSTARTS(STR(?classification), "http://purl.obolibrary.org/obo/GO_"))
      }
      LIMIT 30

architectural_notes:
  schema_design:
    - [Concise bullet point about entity relationships]
    - [Key pattern or hub entity]
  
  performance:
    - [Query optimization tip]
    - [Index-friendly pattern]
  
  data_integration:
    - [External database mapping]
    - [Cross-reference pattern]
  
  data_quality:
    - [Data type quirk or issue]
    - [Missing data pattern]

data_statistics:
  # Entity counts
  total_<entity_type>: <count>
  <subset>_<entity_type>: <count>
  
  # Coverage (use sampling)
  coverage:
    <entities>_with_<property>: "~XX%"
    <entities>_with_<descriptor>: ">YY%"
    
  # Cardinality
  cardinality:
    avg_<related>_per_<entity>: X.X
    max_<related>_per_<entity>: XXXX
    
  # Performance patterns
  performance_characteristics:
    - "Performance observation from testing"
    - "Query optimization recommendation"
    
  # Data quality
  data_quality_notes:
    - "Data type or completeness note"
```

## Success Criteria
- All SPARQL queries execute successfully and return results  
- Shape expressions accurately reflect the actual data structure with minimal redundant comments
- Sample RDF entries are real instances from the database (exactly 5)
- SPARQL queries are tested and working (exactly 7, covering different complexity levels)
- Cross-references comprehensively documented by RDF pattern with all databases listed by category
- Architectural notes in structured YAML format (not prose)
- Data statistics include coverage, cardinality, and performance notes
- Statistics gathered efficiently using sampling (under 10 minutes)
- File is properly formatted YAML that validates  
- Documentation is compact yet sufficient for practical use
- File size is optimized through pattern-based organization while maintaining completeness

## Example of Good vs Bad Commenting

**❌ BAD (Over-commented):**
```shex
<StrainShape> {
  a [ schema:Strain ] ;                         # Type declaration for strain
  rdfs:label xsd:string ;                       # Human-readable label
  schema:hasBacDiveID xsd:integer ;             # Unique BacDive identifier
  schema:hasGenus xsd:string ;                  # Taxonomic genus
  schema:hasSpecies xsd:string ;                # Taxonomic species
}
```

**✅ GOOD (Minimal necessary comments):**
```shex
<StrainShape> {
  a [ schema:Strain ] ;
  rdfs:label xsd:string ;
  schema:hasBacDiveID xsd:integer ;
  schema:hasGenus xsd:string ;
  schema:hasSpecies xsd:string ;
  schema:hasTaxID . ;                           # Mixed types (integer/string)
}
```

## Remember
**The goal is to create an MIE file that is:**
- **Compact**: No unnecessary bloat
- **Complete**: All essential information present
- **Clear**: Easy to understand and use
- **Correct**: All examples tested and verified
- **Actionable**: Statistics directly help query writing

**If documentation doesn't help users write better queries, consider omitting it.**