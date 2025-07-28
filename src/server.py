import requests
import httpx
import json
import sys
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Annotated
from pydantic import Field

# Initialize the FastMCP server
# This is the entry point for the MCP server, which will handle requests and provide tools.
server = FastMCP("RDF Portal MCP Server")

# --- Constants and Configuration (Consolidated) ---
# The SPARQL endpoints for various RDF databases. These endpoints are used to query the RDF data.
# See also: https://github.com/rdfportal/rdfportal.github.io/blob/feature/legacy/info/ep_dataset_graph.tsv
SPARQL_ENDPOINT = {
    "uniprot": "https://rdfportal.org/backend/sib/sparql",
    "pubchem": "https://rdfportal.org/backend/pubchem/sparql",
    "pdb": "https://rdfportal.org/backend/pdb/sparql",
    "chembl": "https://rdfportal.org/backend/ebi/sparql",
    "chebi": "https://rdfportal.org/backend/ebi/sparql",
    "mesh": "https://rdfportal.org/primary/sparql",
    "go": "https://rdfportal.org/primary/sparql",
    "taxonomy": "https://rdfportal.org/primary/sparql"
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

# The Shex files are used to define the shape expressions for SPARQL queries. 
SHEX_FILES = {
    "pubchem": "resources/pubchem.shexj",
    "uniprot": "resources/uniprot.shexj",
    "pdb": "resources/pdb.shexj" # not available yet
}
SHEX_SPARQL_TEMPLATE="resources/shex_sparql_template.yaml"

# Example entries for RDF databases
EXAMPLE_ENTRIES = {
    "chebi": ["http://purl.obolibrary.org/obo/CHEBI_27744", "http://purl.obolibrary.org/obo/CHEBI_75974"],
    "pubchem": ["http://rdf.ncbi.nlm.nih.gov/pubchem/compound/CID2519", "http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay/AID1"],
    "uniprot": ["http://purl.uniprot.org/uniprot/Q9NYK1", "http://purl.uniprot.org/uniprot/P0A7Y3"],
    "pdb": ["http://rdf.wwpdb.org/pdb/101M","http://rdf.wwpdb.org/pdb/1D3Z"],
    "chembl": ["http://rdf.ebi.ac.uk/resource/chembl/assay/CHEMBL1176701","http://rdf.ebi.ac.uk/resource/chembl/target/CHEMBL1906"],
    "mesh": ["http://id.nlm.nih.gov/mesh/2025/A01.378.100"],
    "go": ["http://purl.obolibrary.org/obo/GO_0008150", "http://purl.obolibrary.org/obo/GO_0003674"],
    "taxonomy": ["http://identifiers.org/taxonomy/116609", "http://identifiers.org/taxonomy/9606"]
}

# --- General Prompt ---
@server.prompt(name="General Prompt for RDF Portal MCP Server")
def general_prompt() -> str:
    """
    General prompt for the RDF Portal MCP Server.
    This prompt provides an overview of the available tools and their usage.
    """
    return (
        "Welcome to the RDF Portal MCP Server! "
        "You can use the following tools to interact with RDF data:\n"
        "- `get_sparql_endpoints`: Get available SPARQL endpoints.\n"
        "- `execute_sparql`: Execute a SPARQL query on a specified endpoint.\n"
        "- `run_example_query`: Run an example SPARQL query on a specific RDF database.\n"
        "- `get_graphs_in_database`: Get named graphs in a specific RDF database.\n"
        "- `get_pubchem_compound_id`: Get PubChem compound ID by name.\n"
        "- `get_compound_attributes_from_pubchem`: Get compound attributes from PubChem RDF.\n"
        "- `search_uniprot_entity`: Search for a UniProt entity ID by query.\n"
        "- `search_pdb_entity`: Search for PDBj entry information by keywords.\n"
        "- `describe_pdb_rdf_schema`: Describe the PDB RDF schema.\n"
        "- `search_chembl_entity`: Search for ChEMBL ID by query.\n"
        "- `get_chembl_entity_by_id`: Get ChEMBL entity by ID.\n"
        "For SPARQL queries, you can use the following common prefixes:\n"
        f"{COMMON_PREFIXES}\n"
        "When constructing SPARQL queries, please ensure that you use the correct prefixes and URIs. "
        "Use type conversion such as xsd:integer() or xsd:dateTime() in your queries when appropriate."
    )

@server.prompt(name="Generate ShEx and SPARQL Examples for RDF Database")
def generate_shex_and_sparql_examples(
    dbname: Annotated[str, Field(title="Database Name", description=f"The name of the database for which to generate examples. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    f"""
    Generate ShEx and SPARQL examples for a specific RDF database.

    Args:
        dbname (str): The name of the database for which to generate examples. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: The generated examples in JSON format.
    """
    with open(SHEX_SPARQL_TEMPLATE, "r") as file:
        shex_sparql_template = file.read()
    
    return (
    f"Explore the shape expression for the {dbname} RDF schema as deeply as possible."
    "Construct and run several SPARQL queries based on the shape expression to retrieve biologically relevant data."
    "Make sure the SPARQL queries are well-formed and return meaningful results."
    "Save the obtained shape expressions, along with the SPARQL query examples,"
    "in YAML format so that you can reference them later."
    "The YAML file should be based on the following template:"
    "\n\n"
    f"{shex_sparql_template}"
    "\n\n"
    "During exploration, study at least five diversified entries so the results are more comprehensive."
    "Use `get_sparql_endpoints` to find available SPARQL endpoints."
    "Start by running the `run_example_query` tool to get a feel for the data structure."
    )

# --- Tools for RDF Portal ---

@server.tool()
async def get_sparql_endpoints() -> str:
    """ Get the available SPARQL endpoints for RDF Portal. 
    Returns:
        str: A JSON-formatted string containing the available SPARQL endpoints.
    """
    return json.dumps(SPARQL_ENDPOINT)

@server.tool()
async def execute_sparql(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    endpoint_key: Annotated[str, Field(description="The key for the SPARQL endpoint to use. To find the supported endpoints, use the `get_sparql_endpoints` tool.")]
) -> str:
    """ Execute a SPARQL query on RDF Portal. 
    Args:
        sparql_query (str): The SPARQL query to execute.
        endpoint_key (str): The key for the SPARQL endpoint to use. To find the supported endpoints, use the `get_sparql_endpoints` tool.
    Returns:
        str: A JSON-formatted string containing the results of the SPARQL query.
    """

    if endpoint_key not in SPARQL_ENDPOINT:
        raise ValueError(f"Unknown endpoint key: {endpoint_key}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPARQL_ENDPOINT[endpoint_key], data={"query": sparql_query}, headers={"Accept": "application/sparql-results+json"}
        )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]
    # For an example of "bindings", see:
    # https://rdfportal.org/backend/pdb/sparql?default-graph-uri=&query=PREFIX+PDBo%3A+%3Chttp%3A%2F%2Frdf.wwpdb.org%2Fschema%2Fpdbx-v50.owl%23%3E%0D%0A%0D%0ASELECT+%3Ftype_value+%28COUNT%28%3Fpoly%29+as+%3Fcount%29+WHERE+%7B%0D%0A++%3Fentry+a+PDBo%3Adatablock+.%0D%0A++%3Fentry+PDBo%3Ahas_entity_polyCategory+%3Fpoly_cat+.%0D%0A++%3Fpoly_cat+PDBo%3Ahas_entity_poly+%3Fpoly+.%0D%0A++%3Fpoly+PDBo%3Aentity_poly.type+%3Ftype_value+.%0D%0A%7D+GROUP+BY+%3Ftype_value+ORDER+BY+DESC%28%3Fcount%29&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on
    if not bindings:
        return json.dumps([])
    results = [{key: binding[key]["value"] for key in binding} for binding in bindings]
    return json.dumps(results)

@server.tool()
async def run_example_query(
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
    SELECT *
    WHERE {{
        VALUES ?s {{ {entries} }}
        ?s ?p ?o .
        FILTER (!isBlank(?o))
    }} LIMIT 20
    """
    return await execute_sparql(sparql_query, dbname)

# --- Tools for SPARQL Shape Expressions --- The ShEx files are too large. Temporarily commented out.
# @server.prompt(name="Query by SPARQL")
def build_sparql_query() -> str:
    return "When building a SPARQL query, please refer a relevant shape expressions provided with the resource."

# @server.tool()
async def get_sparql_shape_expression(dbname: str) -> str:
    f"""
    Get a shape expression for a specific RDF database in JSON, which can be used to build a SPARQL query.

    Args:
        dbname (str): The name of the database for which to retrieve the shape expression. Supported values are {', '.join(SHEX_FILES.keys())}.

    Returns:
        str: The shape expression in JSON format.
    """
    shex_file = SHEX_FILES.get(dbname)
    if not shex_file:
        raise ValueError(f"Unknown database: {dbname}")
    with open(shex_file, "r") as file:
        shex = file.read()
    return shex

@server.tool()
async def get_graphs_in_database(dbname: str) -> List[str]:
    """
    Get a list of named graphs in a specific RDF database.

    Args:
        dbname (str): The name of the database for which to retrieve the named graphs. Supported values are "pubchem" and "uniprot".

    Returns:
        List[str]: A list of named graph URIs in the specified database.
    """
    sparql_query = '''
SELECT DISTINCT ?graph WHERE {
  GRAPH ?graph {
    ?s ?p ?o .
  }
}'''
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPARQL_ENDPOINT[dbname], data={"query": sparql_query}, headers={"Accept": "application/sparql-results+json"}
        )
    response.raise_for_status()
    result = response.json()["results"]["bindings"]
    return [binding["graph"]["value"] for binding in result]


# --- Tools for PubChem RDF ---
@server.tool()
async def get_pubchem_compound_id(compound_name: str) -> str:
    """
    Get a PubChem compound ID

    Args: Compound name
        example: "resveratrol"

    Returns: PubChem Compound ID in the JSON format
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/cids/JSON"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
    return response.text

@server.tool()
async def get_compound_attributes_from_pubchem(pubchem_compound_id: str) -> str:
    """
    Get compound attributes from PubChem RDF

    Args: PubChem Compound ID
        example: "445154"

    Returns: Compound attributes in the JSON format
    """
    url = "https://togodx.dbcls.jp/human/sparqlist/api/metastanza_pubchem_compound"
    params = {"id": pubchem_compound_id}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.text

# --- Tools for UniProt RDF ---
@server.tool()
async def search_uniprot_entity(query: str) -> str:
    """
    Search for a UniProt entity ID by its query.

    Args:
        query (str): The query to search for. The query should be unambiguous enough to uniquely identify the entity.

    Returns:
        str: The UniProt protein entity ID corresponding to the given query."
    """
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "fields": "accession,protein_name,gene_names,organism_name",
        "format": "json",
        "size": 50  # optional, limit results
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract just the primary accession ID from each result
    uniprot_ids = [entry.get("primaryAccession") for entry in data.get("results", []) if "primaryAccession" in entry]
    return json.dumps(uniprot_ids)

# --- PDB-specific Tools  ---
@server.tool()
async def search_pdb_entity(db: str, query: str, limit: int = 20) -> str:
    """
    Search for PDBj entry information by keywords.

    Args:
        db (str): The database to search in. Allowed values are:
            - "pdb" (Protein Data Bank, protein structures)
            - "cc" (Chemical Component Dictionary, chemical components or small molecules in PDB)
            - "prd" (BIRD, Biologically Interesting Reference Molecule Dictionary, mostly peptides).
        query (str): Query string, any keywords that can be used to search for PDB entries.
        limit (int): The maximum number of results to return. Default is 20.

    Returns:
        str: A JSON-formatted string containing the search results.
    """
    url = f"https://pdbj.org/rest/newweb/search/{db}?query={query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
#    return response.json()["results"]
    # Parse the response as JSON
    total_results = response.json().get("total", 0)
    result_list = [{entry[0]: entry[1]} for entry in response.json().get("results", [])[:limit]]
    response_dict = {"total": total_results, "results": result_list}
    return json.dumps(response_dict)

@server.tool()
async def describe_pdb_rdf_schema() -> str:
    """
    Describe the PDB RDF schema.

    Returns:
        str: A description of the PDB RDF schema.
    """
    return (
        "The PDB RDF schema is defined in the PDBx-v50.owl file. "
        "RDF triples in the PDB database typically follow this structure:\n"
        """?entry rdf:type PDBo:datablock ;
        PDBo:has_xxxCategory ?category .
        ?category PDBo:has_xxx ?xxx .
        ?xxx PDBo:xxx.property_name ?property_value . """
    )

# ChEMBL-specific tools are not implemented yet, but can be added in the future.
@server.tool()
async def search_chembl_entity(query: str, limit: int = 20) -> str:
    """
    Search for ChEMBL ID by query.

    Args:
        query (str): The query string to search for.
        limit (int): The maximum number of results to return. Default is 20.

    Returns:
        str: A JSON-formatted string containing the search results.
    """
    url = "https://www.ebi.ac.uk/chembl/api/data/chembl_id_lookup.json"
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.text

@server.tool()
async def get_chembl_entity_by_id(service: str, chembl_id: str) -> str:
    """
    Get ChEMBL entity by ID.

    Args:
        service (str): The service to use for the search. Supported values are:
            - "activity" (for ChEMBL activity search, activity ID is an integer; remove the "CHEMBL" or "CHEMBL_ACT" prefixes)
            - "assay" (for ChEMBL assay search)
            - "assay_class" (for ChEMBL assay class search)
            - "atc_class" (for ChEMBL ATC class search)
            - "binding_site" (for ChEMBL binding site search)
            - "biotherapeutic" (for ChEMBL biotherapeutic search)
            - "cell_line" (for ChEMBL cell line search)
            - "chembl_id_lookup" (for ChEMBL ID lookup)
            - "chembl_release" (for ChEMBL release search)
            - "compound_record" (for ChEMBL compound search)
            - "compound_structural_alert" (for ChEMBL compound structural alert search)
            - "document" (for ChEMBL document search)
            - "drug" (for ChEMBL drug search)
            - "drug_indication" (for ChEMBL drug indication search)
            - "drug_warning" (for ChEMBL drug warning search)
            - "go_slim" (for ChEMBL GO slim search)
            - "image" (for ChEMBL image search)
            - "mechanism" (for ChEMBL mechanism search)
            - "metabolism" (for ChEMBL metabolism search)
            - "molecule" (for ChEMBL molecule search)
            - "molecule_form" (for ChEMBL molecule form search)
            - "organism" (for ChEMBL organism search)
            - "protein_classification" (for ChEMBL protein classification search)
            - "source" (for ChEMBL source search)
            - "target" (for ChEMBL target search)
            - "target_relation" (for ChEMBL target relation search)
            - "tissue" (for ChEMBL tissue search)
            - "xref_source" (for ChEMBL cross-reference source search)

        chembl_id (str): The ChEMBL ID to search for.

    """
    url = f"https://www.ebi.ac.uk/chembl/api/data/{service}/{chembl_id}.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    server.run()