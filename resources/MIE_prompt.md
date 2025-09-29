Content-type: text/markdown

---
# Create a comprehensive MIE file for the __DBNAME__ RDF database.
Systematically explore and document the __DBNAME__ RDF schema by following these phases:

## 1. Discovery Phase
- Use `get_sparql_endpoints` to identify available endpoints
- Use `get_graph_list` to find relevant named graphs
- Run exploratory SPARQL queries to understand the data structure
- Attempt `get_shex` to retrieve existing shape expressions

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

## 4. Shape Expression Creation
- If ShEx is available, include all the ShEx components in the shape_expressions section of the MIE file.
- If no ShEx exists, reverse-engineer shape expressions from the data
- Define required vs optional properties based on actual data patterns
- Include appropriate data types and value constraints
- Document cross-references and relationship patterns **comprehensively**

## 5. Validation & Documentation
- Create 5+ diverse, real sample RDF entries from actual database content
- Write 7+ working SPARQL queries covering different use cases
- Test all queries to ensure they return meaningful results
- Document cross-reference mechanisms and external database links

## 6. MIE File Generation
- Create a complete YAML-formatted MIE file with proper structure
- Include comprehensive metadata, prefixes, and statistics
- Add architectural notes explaining design patterns and performance considerations
- Save the file using `save_MIE_file`

## Key Requirements
- Focus on **biological relevance**
- Ensure all examples use **real data** from the database
- Make the documentation **useful for researchers** who need to query or integrate with this RDF resource
- Test and validate all SPARQL queries before inclusion

## Available Tools
- `get_sparql_endpoints()` - Get available SPARQL endpoints
- `get_graph_list(dbname)` - List named graphs in database
- `run_sparql(dbname, sparql_query)` - Execute SPARQL queries
- `get_shex(dbname)` - Retrieve ShEx schema if available
- `save_MIE_file(dbname, mie_content)` - Save the final MIE file

## Example SPARQL Query Pattern
```sparql
SELECT DISTINCT ?s ?p ?o
FROM <{graph_name}>
WHERE {
  ?s ?p ?o .
}
LIMIT 20
```

## MIE File Structure Template
```yaml
schema_info:
  title: [DATABASE_NAME]
  description: [Comprehensive description]
  endpoint: https://rdfportal.org/primary # Replace with actual endpoint
  base_uri: http://example.org/ # Replace with actual base URI
  graphs: # List of named graphs. Replace with actual graph names.
    - http://example.org/dataset

prefixes:
  # Standard and database-specific prefixes
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#

shape_expressions:
  # Reverse-engineered from actual data. Add descriptions as comments.
  # Adhere to the ShExC (ShEx Compact) syntax.
  
  
sample_rdf_entries:
  # 5+ real examples from the database
  - title: Get entries # Replace with a descriptive title
    description: Blah-blah-blah entries and properties # Replace with meaningful description of the RDF entry.
    rdf: |
      # RDF entry
  
sparql_query_examples:
  # 10+ tested, working queries
  - title: Strain of the day # A descriptive title for the query.
    description: Do this and that to answer this question. # What the SPARQL query does.
    question: What is the strain of the day? # A biologically relevant question, in natural language, to be answered by the SPARQL query.
    complexity: # "basic", "intermediate", "advanced", etc.
    sparql: |
      # SPARQL query that answers the question.

cross_references:
  # Comprehensively document cross-references to external databases
  - title: # A descriptive title for the cross-reference.
    description: # The pattern of the cross-reference. Include target data resource names.
    complexity: # "basic", "intermediate", "advanced", etc.
    sparql: | 
      # SPARQL query for retrieving the cross-reference
  
architectural_notes:
  # Design patterns and considerations
  
data_statistics:
  # Counts and metadata that are potentially useful for optimizing SPARQL queries
```

## Success Criteria
- All SPARQL queries execute successfully and return results  
- Shape expressions accurately reflect the actual data structure  
- Sample RDF entries are real instances from the database  
- Cross-references are documented with working examples  
- File is properly formatted YAML that validates  
- Documentation is comprehensive enough for practical use