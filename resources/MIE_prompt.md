# Create a compact yet comprehensive MIE file for __DBNAME__ RDF database.

## Philosophy: Essential over Exhaustive
Create documentation that is **compact, clear, and complete** - sufficient for researchers to effectively query the database without unnecessary bloat.

## 1. Discovery Phase (CRITICAL: Follow Systematically)

**⚠️ WARNING: Avoid Sampling Bias and Premature Conclusions**
- The first 50 results from a SPARQL query may NOT represent the entire database
- Always verify comprehensively using multiple query patterns before drawing conclusions
- Check ontology graphs for class definitions BEFORE sampling data
- Never assume timeouts mean "data doesn't exist"

### 1.1 Systematic Discovery Workflow

**Step 1: Check for Existing Documentation** (2 minutes)
- Use `get_sparql_endpoints()` to identify available endpoints
- Use `get_graph_list(dbname)` to find ALL named graphs (data + ontology graphs)
- Attempt `get_shex(dbname)` to retrieve existing shape expressions
- Attempt `get_MIE_file(dbname)` to retrieve existing MIE files
  - **If an existing MIE file is found**: Perform compliance check (see section 1.2 below)
  - **If compliant**: Update/improve the file as needed
  - **If non-compliant**: Create a new MIE file from scratch

**Step 2: Discover Schema/Ontology Definitions** (5 minutes)
```sparql
# Query 1: Get all RDF classes from ontology graphs
SELECT DISTINCT ?class
FROM <ontology_graph_uri>
WHERE {
  ?class a owl:Class .
}
LIMIT 100

# Query 2: Get all properties from ontology graphs
SELECT DISTINCT ?property ?type
FROM <ontology_graph_uri>
WHERE {
  ?property a ?type .
  FILTER(?type IN (owl:ObjectProperty, owl:DatatypeProperty, rdf:Property))
}
LIMIT 100

# Query 3: Sample property domains and ranges
SELECT ?property ?domain ?range
FROM <ontology_graph_uri>
WHERE {
  ?property rdfs:domain ?domain ;
            rdfs:range ?range .
}
LIMIT 100
```

**Why this matters**: Ontology graphs reveal what SHOULD exist, preventing you from missing entire entity types.

**Step 3: Explore URI Patterns** (5 minutes)

Test multiple URI namespace patterns to discover different entity types:

```sparql
# Pattern 1: identifiers.org/[namespace]
SELECT ?s ?p ?o
WHERE {
  ?s ?p ?o .
  FILTER(STRSTARTS(STR(?s), "http://identifiers.org/"))
}
LIMIT 50

# Pattern 2: Database-specific namespace
SELECT ?s ?p ?o  
WHERE {
  ?s ?p ?o .
  FILTER(STRSTARTS(STR(?s), "http://[database-specific-uri]/"))
}
LIMIT 50

# Pattern 3: Sample different prefixes found in ontology
SELECT ?s ?type
WHERE {
  ?s a ?type .
}
LIMIT 100
```

**Why this matters**: Different URI patterns often indicate different data layers (e.g., identifiers vs full records vs features).

**Step 4: Systematic Class Instance Sampling** (10 minutes)

For EACH class discovered in Step 2, sample actual instances:

```sparql
# For each class found:
SELECT ?instance ?p ?o
WHERE {
  ?instance a <ClassURI> .
  ?instance ?p ?o .
}
LIMIT 50
```

**Why this matters**: Prevents assuming the database only contains what you see first. Some classes may have millions of instances, others only a few.

**Step 5: Verify and Cross-Check** (5 minutes)

If queries timeout or return no results:
- ✅ Try with smaller LIMIT values
- ✅ Try without FROM clauses
- ✅ Try with different FILTER patterns
- ✅ Sample from different graph URIs
- ❌ DON'T assume "no results = doesn't exist"

### 1.2 MIE File Compliance Check

When an existing MIE file is retrieved, verify it complies with these instructions:

**Structure & Format:**
- [ ] Properly formatted YAML that validates
- [ ] Contains all required sections: schema_info, shape_expressions, sample_rdf_entries, sparql_query_examples, cross_references, architectural_notes, data_statistics
- [ ] Follows the MIE File Structure Template

**Sample RDF Entries:**
- [ ] Exactly 5 examples (not more, not fewer)
- [ ] Covers diverse categories: core entity, related entity, sequence/molecular data, cross-reference, geographic/temporal
- [ ] Uses real data from the database
- [ ] Descriptions are concise (1-2 sentences)

**SPARQL Query Examples:**
- [ ] Exactly 7 queries total
- [ ] Includes required query: keyword filtering for entry IDs
- [ ] Includes required query: biological/functional annotations for given entry IDs
- [ ] Does NOT include external cross-reference queries (should be in Cross-references section only)
- [ ] Distribution: 2 basic, 3 intermediate, 2 advanced
- [ ] All queries have been tested and return results
- [ ] Each query has: title, description, question, complexity level, working SPARQL code

**Shape Expressions:**
- [ ] Minimal redundant comments (only non-obvious properties commented)
- [ ] No comments like "# Unique identifier" for obvious properties
- [ ] Comments are one line maximum
- [ ] Proper ShExC syntax
- [ ] Covers ALL major entity types discovered (not just the first one found)

**Cross-references:**
- [ ] Organized by RDF pattern (not by individual database)
- [ ] Comprehensive coverage of all external databases
- [ ] Databases grouped by category within each pattern
- [ ] One representative SPARQL query per pattern
- [ ] Includes coverage information where relevant

**Architectural Notes:**
- [ ] Structured YAML format with exactly 4 categories: schema_design, performance, data_integration, data_quality
- [ ] Uses bullet points (NOT prose paragraphs)
- [ ] No markdown headers or formatting within section
- [ ] Each bullet is concise (one line when possible)

**Data Statistics:**
- [ ] Includes entity counts for major types
- [ ] Includes coverage estimates (using sampling, expressed as ranges like "~95%")
- [ ] Includes cardinality (avg/max) for one-to-many relationships
- [ ] Includes performance_characteristics from query testing
- [ ] Statistics are actionable for query writing
- [ ] No overly detailed breakdowns or exact percentages when estimates suffice

**Overall Quality:**
- [ ] Compact: no unnecessary bloat
- [ ] Complete: all essential information present (covers ALL entity types, not just some)
- [ ] Clear: easy to understand and use
- [ ] Correct: examples tested and verified
- [ ] Actionable: statistics help query writing

**Decision:**
- If ≥90% of checks pass and issues are minor: Update/improve the existing file
- If <90% of checks pass or major structural issues: Create new MIE file from scratch

## 2. Schema Analysis (DO NOT SKIP)

**Critical First Step: Get Complete Class Inventory**
```sparql
# From ontology graph
SELECT ?class (COUNT(?instance) as ?count)
WHERE {
  ?instance a ?class .
}
GROUP BY ?class
ORDER BY DESC(?count)
```

**If the above times out, try sampling:**
```sparql
SELECT DISTINCT ?class
WHERE {
  ?s a ?class .
}
LIMIT 100
```

Then for each class:
- Query for sample instances
- Examine property patterns
- Identify required vs optional properties
- Check for hierarchical relationships

## 3. Deep Dive Investigation

For EACH major entity type discovered:

### 3.1 Property Analysis
```sparql
# Get all properties used by this entity type
SELECT DISTINCT ?property (COUNT(?value) as ?usage)
WHERE {
  ?entity a <EntityType> .
  ?entity ?property ?value .
}
GROUP BY ?property
ORDER BY DESC(?usage)
LIMIT 50
```

### 3.2 Relationship Mapping
```sparql
# Find relationships between entity types
SELECT ?type1 ?property ?type2 (COUNT(*) as ?count)
WHERE {
  ?entity1 a ?type1 .
  ?entity1 ?property ?entity2 .
  ?entity2 a ?type2 .
}
GROUP BY ?type1 ?property ?type2
ORDER BY DESC(?count)
LIMIT 50
```

### 3.3 External Cross-Reference Patterns
```sparql
# Identify external database links
SELECT DISTINCT ?property ?externalURL
WHERE {
  ?entity ?property ?externalURL .
  FILTER(isIRI(?externalURL))
  FILTER(!STRSTARTS(STR(?externalURL), STR(<database_base_uri>)))
}
LIMIT 100
```

## 4. Shape Expression Creation (Efficiency Guidelines)

- If ShEx is available, include all the ShEx components in the shape_expressions section
- If no ShEx exists, reverse-engineer shape expressions from the data
- Define required vs optional properties based on actual data patterns
- Include appropriate data types and value constraints
- **CRITICAL**: Create shapes for ALL major entity types, not just the first one you find

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
- **Cover different entity types if database has multiple layers**

### SPARQL Query Examples (Target: Exactly 7 queries)
Create 7 queries with this distribution:
- **2 basic**: Simple retrieval, filtering (e.g., get entities by type, basic property filtering)
- **3 intermediate**: Aggregation, grouping, moderate filtering (e.g., count by category, find entities in range)
- **2 advanced**: Complex joins, multiple patterns, nested queries (e.g., multi-entity integration, federated patterns)

**Required Queries** (must include these 2):
1. **Keyword filtering query**: Obtain entry IDs by filtering with keywords (e.g., search by label, description, or text fields)
2. **Biological annotations query**: Obtain biological/functional annotations for given entry IDs (e.g., functions, roles, classifications, descriptions)

**Additional Query Categories** (select 5 from these):
1. Taxonomic/hierarchical retrieval
2. Phenotypic/characteristic filtering
3. Sequence data integration
4. Geographic distribution
5. Aggregation/statistics
6. Multi-entity complex integration

**Note:** Do not include external cross-references queries here, as they are covered in the Cross-references section.

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
    - Multi-layered architecture (if applicable)
  
  performance:
    - Which queries are optimized
    - Index-friendly patterns
    - Query optimization tips
    - Known timeout patterns
  
  data_integration:
    - External database mappings
    - Cross-reference patterns
    - Integration points
    - Federation capabilities
  
  data_quality:
    - Known data type issues
    - Missing data patterns
    - Validation notes
    - Completeness variations across entity types
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
- **Count ALL entity types discovered, not just the first one**

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
  # A. Entity Counts (required - ALL types)
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
- [ ] Entity counts for all major types (not just the first one discovered)
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
- **Ensure documentation covers ALL entity types discovered, not just a subset**
- Save the file using `save_MIE_file`

## Key Requirements
- **ALWAYS check ontology graphs for class definitions FIRST**
- **Explore multiple URI patterns before concluding what exists**
- **Check existing MIE files for compliance** before creating new ones
- Focus on **biological relevance**
- Ensure all examples use **real data** from the database
- **Prioritize compactness**: Essential over exhaustive
- Test and validate all SPARQL queries before inclusion
- Use **sampling** for expensive statistics
- Make documentation **immediately useful** for query writing
- **Never assume first results represent the entire database**

## Efficiency Checklist Before Saving
- [ ] Checked ontology graph(s) for complete class inventory
- [ ] Explored multiple URI patterns to discover all entity types
- [ ] Verified conclusions with cross-checking queries
- [ ] ShEx has minimal redundant comments (only non-obvious properties commented)
- [ ] Exactly 5 diverse RDF examples (not 6, not 8) covering different entity types
- [ ] Exactly 7 SPARQL queries covering different complexity levels
- [ ] Includes required queries: keyword filtering and biological annotations
- [ ] No cross-reference queries in SPARQL examples (covered in Cross-references section)
- [ ] Comprehensive cross-references organized by RDF pattern with all databases listed
- [ ] Architectural notes in structured YAML format (no prose paragraphs)
- [ ] Data statistics with coverage, cardinality, and performance notes
- [ ] Entity counts for ALL major types (not just some)
- [ ] Used sampling for expensive statistics (kept under 10 minutes total)
- [ ] All descriptions are concise (1-2 sentences)
- [ ] All SPARQL queries have been tested and work

## Common Pitfalls to Avoid

### ❌ Sampling Bias
**Problem**: Assuming first 50 results represent entire database
**Solution**: Check ontology graphs, explore multiple URI patterns, verify with counts

### ❌ Premature Conclusions
**Problem**: Query timeout interpreted as "data doesn't exist"
**Solution**: Try smaller LIMITs, different patterns, alternative graph URIs

### ❌ Single Pattern Exploration
**Problem**: Only checking one URI namespace pattern
**Solution**: Test identifiers.org, database-specific URIs, feature URIs, etc.

### ❌ Ignoring Ontology Graphs
**Problem**: Missing entity types that have few instances
**Solution**: ALWAYS query ontology graphs for class definitions first

### ❌ Incomplete Entity Coverage
**Problem**: Documenting only the most obvious entity type
**Solution**: Create shapes and examples for ALL major entity types

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
     - Main entity types (ALL of them)
     - Primary use cases
     - Key features
     - Multi-layered structure if applicable]
  endpoint: https://rdfportal.org/primary # Replace with actual endpoint
  base_uri: http://example.org/ # Replace with actual base URI
  graphs: # List of named graphs (data AND ontology)
    - http://example.org/dataset
    - http://example.org/ontology

shape_expressions: |
  # Reverse-engineered from actual data
  # Include all standard and database-specific PREFIXes
  # Comment only non-obvious properties or complex patterns
  # Adhere to ShExC (ShEx Compact) syntax
  # CREATE SHAPES FOR ALL MAJOR ENTITY TYPES
  
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  
  <PrimaryEntityShape> {
    a [ schema:EntityType ] ;
    rdfs:label xsd:string ;
    schema:property xsd:string ;           # Only comment when needed
    schema:complexProperty @<OtherShape>   # Relationships
  }
  
  <SecondaryEntityShape> {
    # If database has multiple entity types, document them all
  }

sample_rdf_entries:
  # Exactly 5 diverse examples (one per category)
  # ENSURE examples cover different entity types if applicable
  - title: [Descriptive title]
    description: [Concise 1-2 sentence description]
    rdf: |
      # Real RDF instance from database
  
  - title: [Another example - different entity type]
    description: [Brief description]
    rdf: |
      # Real RDF instance

sparql_query_examples:
  # Exactly 7 queries: 2 basic, 3 intermediate, 2 advanced
  # ENSURE queries cover different entity types if applicable
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
      # ... list other categories
    complexity: basic
    sparql: |
      # Representative query for this pattern

architectural_notes:
  schema_design:
    - [Concise bullet about entity relationships]
    - [Multi-layer architecture if applicable]
  
  performance:
    - [Query optimization tip]
    - [Known timeout patterns]
  
  data_integration:
    - [External database mapping]
    - [Cross-reference pattern]
  
  data_quality:
    - [Data type quirk or issue]
    - [Completeness variations across types]

data_statistics:
  # Entity counts - ALL TYPES
  total_<entity_type_1>: <count>
  total_<entity_type_2>: <count>
  total_<entity_type_3>: <count>
  
  # Coverage (use sampling)
  coverage:
    <entities>_with_<property>: "~XX%"
    
  # Cardinality
  cardinality:
    avg_<related>_per_<entity>: X.X
    
  # Performance patterns
  performance_characteristics:
    - "Observation from testing"
    
  # Data quality
  data_quality_notes:
    - "Brief note on issues"
```

## Success Criteria
- **Ontology graph(s) checked for complete class inventory**
- **Multiple URI patterns explored to discover all entity types**
- All SPARQL queries execute successfully and return results  
- Shape expressions accurately reflect the actual data structure with minimal redundant comments
- **Shape expressions cover ALL major entity types, not just the first discovered**
- Sample RDF entries are real instances from the database (exactly 5)
- **Sample RDF entries cover different entity types if database has multiple layers**
- SPARQL queries are tested and working (exactly 7, covering different complexity levels)
- Required queries included: keyword filtering for entry IDs and biological annotations for given IDs
- No redundant cross-reference queries (covered in dedicated Cross-references section)
- Cross-references comprehensively documented by RDF pattern with all databases listed by category
- Architectural notes in structured YAML format (not prose)
- Data statistics include coverage, cardinality, and performance notes
- **Statistics cover ALL entity types discovered**
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
- **Complete**: All essential information present (including ALL entity types)
- **Clear**: Easy to understand and use
- **Correct**: All examples tested and verified
- **Actionable**: Statistics directly help query writing
- **Comprehensive**: Covers entire database structure, not just a subset

**If documentation doesn't help users write better queries, consider omitting it.**

**NEVER assume the first results you see represent the entire database. Always verify systematically.**