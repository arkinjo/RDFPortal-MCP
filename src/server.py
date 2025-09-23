import httpx
import json
from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field

# Initialize the FastMCP server
# This is the entry point for the MCP server, which will handle requests and provide tools.
mcp = FastMCP("RDF Portal MCP Server")

@mcp.resource("resource://greeting")
def greeting() -> str:
    return "Hello! I don't know why this is here. But, the server doesn't work without it."

# --- Constants and Configuration (Consolidated) ---
# The SPARQL endpoints for various RDF databases. These endpoints are used to query the RDF data.
# See also: https://github.com/rdfportal/rdfportal.github.io/blob/feature/legacy/info/ep_dataset_graph.tsv
SPARQL_ENDPOINT = {
    "uniprot": "https://rdfportal.org/backend/sib/sparql",
    "pubchem": "https://rdfportal.org/backend/pubchem/sparql",
    "pdb": "https://rdfportal.org/backend/pdb/sparql",
    "chembl": "https://rdfportal.org/backend/ebi/sparql",
    "chebi": "https://rdfportal.org/backend/ebi/sparql",
    "reactome": "https://rdfportal.org/backend/ebi/sparql",
    "mesh": "https://rdfportal.org/primary/sparql",
    "go": "https://rdfportal.org/primary/sparql",
    "taxonomy": "https://rdfportal.org/primary/sparql",
    "wikidata": "https://query.wikidata.org/sparql",
    "mondo": "https://rdfportal.org/primary/sparql",
    "ddbj": "https://rdfportal.org/ddbj/sparql",
    "glycosmos": "https://ts.glycosmos.org/sparql",
    "bacdive": "https://rdfportal.org/primary/sparql",
    "mediadive": "https://rdfportal.org/primary/sparql"
}

SPARQL_ENDPOINT_KEYS = list(SPARQL_ENDPOINT.keys())

COMMON_PREFIXES = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX PDBo: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX uniprot: <http://purl.uniprot.org/uniprot/>
"""

# The MIE files are used to define the shape expressions for SPARQL queries. 
MIE_FILES = {
    "uniprot": "mie/uniprot.yaml",
    "pdb": "mie/pdb.yaml",
    "chembl": "mie/chembl.yaml",
    "chebi": "mie/chebi.yaml",
    "go": "mie/go.yaml",
    "mesh": "mie/mesh.yaml",
    "taxonomy": "mie/taxonomy.yaml",
    "wikidata": "mie/wikidata.yaml",
    "pubchem": "mie/pubchem.yaml",
    "reactome": "mie/reactome.yaml",
    "mondo": "mie/mondo.yaml",
    "ddbj": "mie/ddbj.yaml",
    "glycosmos": "mie/glycosmos.yaml",
    "bacdive": "mie/bacdive.yaml",
    "mediadive": "mie/mediadive.yaml"
}

MIE_TEMPLATE="resources/MIE_template.yaml"
RDF_CONFIG_TEMPLATE="rdf-config/template.yaml"

# Example entries for RDF databases
EXAMPLE_ENTRIES = {
    "chebi": ["http://purl.obolibrary.org/obo/CHEBI_27744", "http://purl.obolibrary.org/obo/CHEBI_75974"],
    "pubchem": ["http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID2519", "http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay/AID1"],
    "uniprot": ["http://purl.uniprot.org/uniprot/Q9NYK1", "http://purl.uniprot.org/uniprot/P0A7Y3"],
    "pdb": ["http://rdf.wwpdb.org/pdb/101M","http://rdf.wwpdb.org/pdb/1D3Z"],
    "chembl": ["http://rdf.ebi.ac.uk/resource/chembl/assay/CHEMBL1176701","http://rdf.ebi.ac.uk/resource/chembl/target/CHEMBL1906"],
    "mesh": ["http://id.nlm.nih.gov/mesh/2025/A01.378.100"],
    "go": ["http://purl.obolibrary.org/obo/GO_0008150", "http://purl.obolibrary.org/obo/GO_0003674"],
    "taxonomy": ["http://identifiers.org/taxonomy/116609", "http://identifiers.org/taxonomy/9606"],
    "wikidata": ["http://www.wikidata.org/entity/Q7187", "http://www.wikidata.org/entity/Q40108"],
    "reactome": ["http://www.reactome.org/biopax/68/49646#Pathway227","http://www.reactome.org/biopax/68/49646#BiochemicalReaction1002"],
    "mondo": ["http://purl.obolibrary.org/obo/MONDO_0000831","http://purl.obolibrary.org/obo/MONDO_0004784"],
    "ddbj": ["http://identifiers.org/bioproject/PRJNA594547","http://identifiers.org/biosample/SAMN12636418"],
    "glycosmos": ["http://glycosmos.org/glycogene/25", "http://purl.obolibrary.org/obo/CHEBI_146500"]
}

# -- prompts --

@mcp.prompt(name="Hello RDF Portal!")
def hello() -> str:
    """
    Introduction to the RDF Portal MCP Server.
    This prompt provides an overview of the available tools and their usage.
    """
    return (
        "Welcome to the RDF Portal MCP Server! "
        f"This server has access to the following RDF databases: {', '.join(SPARQL_ENDPOINT.keys())}.\n"
        "You can use the following tools to interact with RDF data:\n"
        "- `get_sparql_endpoints`: Get available SPARQL endpoints.\n"
        "- `run_sparql`: Execute a SPARQL query on a specified endpoint.\n"
        "- `run_example_query`: Run an example SPARQL query on a specific RDF database.\n"
        "- `get_class_list`: Get a list of classes in an RDF database that match a given URI.\n"
        "- `get_property_list`: Get a list of properties in an RDF database that match a given URI.\n"
        "- `get_graph_list`: Get named graphs in a specific RDF database.\n"
        "- `describe_rdf_schema`: Get the RDF schema of a specific RDF database. Use this before constructing SPARQL queries.\n"
        "When constructing SPARQL queries, ensure that you use the correct prefixes and URIs, "
        "start simple, use OPTIONAL extensively, build queries step-by-step, and test with known entities."
        "Use type conversion such as xsd:decimal() or xsd:dateTime() in your queries when appropriate."
    )

@mcp.prompt(enabled=True, name="Generate a MIE file")
def generate_MIE_file(
    dbname: Annotated[str, Field(description=f"The name of the database to explore. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    f"""
    Explore a specific RDF database to generate an MIE file for SPARQL queries.

    Args:
        dbname (str): The name of the database to explore. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: The generated examples in YAML format.
    """
    with open(MIE_TEMPLATE, "r", encoding="utf-8") as file:
        mie_template = file.read()

    return (
    f"Explore the shape expression for the {dbname} RDF schema as deeply as possible"
    "In particular, pay close attention to how cross-references to other databases are handled."
    "Construct and run several SPARQL queries based on the shape expression to retrieve biologically relevant data."
    "Make sure the SPARQL queries are well-formed and return meaningful results."
    "Save the obtained shape expressions, along with the RDF and SPARQL query examples,"
    "in YAML format so that you can reference them later."
    "The YAML file should be based on the following template:"
    "\n\n"
   f"{MIE_TEMPLATE}"
   "\n\n"
   f"{mie_template}"
    "\n\n"
    "Use `get_sparql_endpoints` to find available SPARQL endpoints."
    "Use `run_example_query` to get a feel for the data structure."
    "Then, use `get_class_list`, `get_property_list`, and `get_graphs_in_database` to explore classes, properties, and named graphs in the database."
    "Test all the SPARQL queries and cross-references thoroughly."
    "Also, check if all the RDF examples really exist in the database."
    )

@mcp.prompt(name="Validate SPARQL and RDF examples")
def validate_sparql_and_rdf() -> str:
    """
    Validate SPARQL and RDF examples.
    """
    return """
    Test all the SPARQL query examples and cross-references thoroughly.
    Also, check if all the RDF examples exist in the database.
    """

@mcp.prompt(enabled=True, name="Generate RDF-Config file")
def generate_rdf_config(
        dbname: Annotated[str, Field(description=f"The name of the database for which to generate examples. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    f"""
    Generate the RDF-Config file for a specific RDF database.

    Args:
        dbname (str): The name of the database for which to generate examples. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: The generated examples in YAML format.
    """
    with open(RDF_CONFIG_TEMPLATE, "r", encoding="utf-8") as file:
        template = file.read()
    return (
    f"Study the RDF Schema of {dbname} by exploring the database."
    "Try to make biologically relevant SPARQL queries to explore the database structure."
    "The results should be saved in YAML format."
    "The YAML file should be based on the following template:"
    "\n\n"
   f"{template}"
    "\n\n"
    "Use `get_sparql_endpoints` to find available SPARQL endpoints."
    "Use `run_example_query` to get a feel for the data structure."
    "Then, use `get_class_list`, `get_property_list`, and `get_graphs_in_database` to explore classes, properties, and named graphs in the database."
 
    )

# --- Tools for RDF Portal --- #

@mcp.tool()
async def get_sparql_endpoints() -> str:
    """ Get the available SPARQL endpoints for RDF Portal. 
    Returns:
        str: A JSON-formatted string containing the available SPARQL endpoints.
    """
    return json.dumps(SPARQL_ENDPOINT)

@mcp.tool()
async def get_void(
    graph_uri: Annotated[str,Field(description="Graph URI to explore. Use `get_graph_list` to get appropriate graph URI.")]
) -> list:
    """ Get VoID data for the given graph URI.
    Args:
        graph_uri (str): Graph URI to explore. Use `get_graph_list` to get appropriate graph URI.
    Returns:
        str: A JSON-formatted string containing the VoID data.
    """
    query=f"""
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?total_count ?class_count ?property_count ?class_name ?class_triple_count ?property_name ?property_triple_count
WHERE {{
  VALUES ?gname {{ <{graph_uri}> }}
  [
    a sd:Service ;
    sd:defaultDataset [
       a sd:Dataset ;
       sd:namedGraph [
         sd:name ?gname ;
         a sd:NamedGraph ;
         sd:endpoint ?ep_url ;
         sd:graph [
           a void:Dataset ;
           void:triples ?total_count ;
           void:classes ?class_count ;
           void:properties ?property_count ;
           void:distinctObjects ?uniq_object_count ;
           void:distinctSubjects ?uniq_subject_count ;
           void:classPartition [
             void:class ?class_name ;
             void:entities ?class_triple_count
           ] ;
           void:propertyPartition [
             void:property ?property_name ;
             void:triples ?property_triple_count
           ]
         ]
       ]
     ]
  ] .
}}
"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://plod.dbcls.jp/repositories/RDFPortal_VoID2",
            data={"query": query},
            headers={"Accept": "application/sparql-results+json"}
        )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]
    if not bindings:
        return []
    results = [{key: binding[key]["value"] for key in binding} for binding in bindings]
    return results

# Making this a @mcp.tool() becomes an error, so we keep it as a function.
async def execute_sparql(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    dbname: Annotated[str, Field(description=f"The name of the database to query. To find the supported databases, use the `get_sparql_endpoints` tool. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.")]
) -> list:
    """ Execute a SPARQL query on RDF Portal. 
    Args:
        sparql_query (str): The SPARQL query to execute.
        dbname (str): The name of the database to query. To find the supported databases, use the `get_sparql_endpoints` tool.
    Returns:
        dict: The results of the SPARQL query in JSON.
    """

    if dbname not in SPARQL_ENDPOINT:
        raise ValueError(f"Unknown database: {dbname}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPARQL_ENDPOINT[dbname], data={"query": sparql_query}, headers={"Accept": "application/sparql-results+json"}
        )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]
    # For an example of "bindings", see:
    # https://rdfportal.org/backend/pdb/sparql?default-graph-uri=&query=PREFIX+PDBo%3A+%3Chttp%3A%2F%2Frdf.wwpdb.org%2Fschema%2Fpdbx-v50.owl%23%3E%0D%0A%0D%0ASELECT+%3Ftype_value+%28COUNT%28%3Fpoly%29+as+%3Fcount%29+WHERE+%7B%0D%0A++%3Fentry+a+PDBo%3Adatablock+.%0D%0A++%3Fentry+PDBo%3Ahas_entity_polyCategory+%3Fpoly_cat+.%0D%0A++%3Fpoly_cat+PDBo%3Ahas_entity_poly+%3Fpoly+.%0D%0A++%3Fpoly+PDBo%3Aentity_poly.type+%3Ftype_value+.%0D%0A%7D+GROUP+BY+%3Ftype_value+ORDER+BY+DESC%28%3Fcount%29&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on
    if not bindings:
        return []
    results = [{key: binding[key]["value"] for key in binding} for binding in bindings]
    return results

@mcp.tool(
        enabled=True,
        name="run_sparql",
        description="Run a SPARQL query on a specific RDF database."
)
async def run_sparql(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.")],
) -> list:
    """
    Run a SPARQL query on a specific RDF database. Use `describe_rdf_schema()` to understand the RDF graph structure of the database.

    Args:
        sparql_query (str): The SPARQL query to execute.
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.

    Returns:
        list: The results of the SPARQL query in JSON format.
    """
    return await execute_sparql(sparql_query, dbname)

@mcp.tool()
async def run_example_query(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> list:
    """
    Run an example SPARQL query on a specific RDF database.
    Use this to start exploring the structure and content of the database.
    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.
    Returns:
        list: List of example RDF triples.
 """
    if dbname not in SPARQL_ENDPOINT:
        raise ValueError(f"Unknown database: {dbname}")
    entries = ' '.join(f'<{entry}>' for entry in EXAMPLE_ENTRIES.get(dbname, []))
    sparql_query = f"""
    SELECT ?subject ?predicate ?object
    WHERE {{
        VALUES ?subject {{ {entries} }}
        ?subject ?predicate ?object .
        FILTER (!isBlank(?object))
    }} LIMIT 20
    """
    return await execute_sparql(sparql_query, dbname)

@mcp.tool(enabled=False)
async def get_example_query(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    """
    Run an example SPARQL query on a specific RDF database.
    Use this to start exploring the structure and content of the database.
    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.
    Returns:
        str: The example RDF triples in JSON format.
 """
    if dbname not in SPARQL_ENDPOINT:
        raise ValueError(f"Unknown database: {dbname}")
    entries = ' '.join(f'<{entry}>' for entry in EXAMPLE_ENTRIES.get(dbname, []))
    sparql_query = f"""
    SELECT ?subject ?predicate ?object
    WHERE {{
        VALUES ?subject {{ {entries} }}
        ?subject ?predicate ?object .
        FILTER (!isBlank(?object))
    }} LIMIT 20
    """
    return sparql_query

# --- Tools for exploring RDF databases ---
@mcp.tool(
        enabled=True,
        name="get_class_list",
        description="Get a list of classes in the RDF database that match the given URI."
)
async def get_class_list(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.")],
    uri: Annotated[str, Field(description="The URI to match classes. `http://...`")]) -> list:
    f"""
    Get a list of classes in the RDF database that match the given URI.

    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.
        uri (str): The URI to match classes.

    Returns:
        list: The list of classes.
    """
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?class
    WHERE {{
        ?class a owl:Class .
        FILTER STRSTARTS(STR(?class), "{uri}")
    }} LIMIT 100
    """
    return await execute_sparql(sparql_query, dbname)

@mcp.tool(
        enabled=True,
        name="get_property_list",
        description="Get a list of properties in the RDF database that match the given URI."
)
async def get_property_list(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.")],
    uri: Annotated[str, Field(description="The URI to match properties. `http://...`")]
) -> list:
    f"""
    Get a list of properties in the RDF database that match the given URI.

    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.
        uri (str): The URI to match properties.

    Returns:
        list: The list of properties.
    """
    sparql_query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?property 
    WHERE {{
        ?property a ?proptype .
        ?proptype rdfs:subClassOf rdf:Property .
        FILTER STRSTARTS(STR(?property), "{uri}")
    }} LIMIT 100
    """
    return await execute_sparql(sparql_query, dbname)

@mcp.tool(
        enabled=True,
        name="get_graph_list",
        description="Get a list of named graphs in a specific RDF database."
)
async def get_graph_list(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.")]
    ) -> list:
    f"""
    Get a list of named graphs in a specific RDF database.

    Args:
        dbname (str): The name of the database for which to retrieve the named graphs. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.


    Returns:
        list: The list of named graphs.
    """
    sparql_query = '''
SELECT DISTINCT ?graph WHERE {
  GRAPH ?graph {
    ?s ?p ?o .
  }
}'''
    return await execute_sparql(sparql_query, dbname)

@mcp.tool(
        enabled=True,
        name="describe_rdf_schema",
        description="Use this before constructing SPARQL queries to get the RDF schema of a specific RDF database."
)
async def describe_rdf_schema(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(MIE_FILES.keys())}.")]
    ) -> str:
    f"""
    Get the RDF schema of a specific RDF database in YAML format, which can be used as a hint to build a SPARQL query.

    Args:
        dbname (str): The name of the database for which to retrieve the shape expression. Supported values are {', '.join(MIE_FILES.keys())}.

    Returns:
        str: The RDF schema information in YAML format.
    """
    mie_file = MIE_FILES.get(dbname)
    if not mie_file:
        raise ValueError(f"Unknown database: {dbname}")
    try:
        with open(mie_file, "r", encoding="utf-8") as file:
            content = file.read()
            response_text = f"""Content-type: application/yaml; charset=utf-8
{content}"""
            return response_text
    except FileNotFoundError:
        return f"Error: The schema file for '{dbname}' was not found at the path '{mie_file}'."


if __name__ == "__main__":
    mcp.run()