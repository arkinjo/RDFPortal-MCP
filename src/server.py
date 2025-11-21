import httpx
import json
import os
import yaml
import sys
from fastmcp import FastMCP
from typing import Annotated, List, Dict, Any
from pydantic import Field

# Initialize the FastMCP server
# This is the entry point for the MCP server, which will handle requests and provide tools.
mcp = FastMCP("RDF Portal MCP Server")

@mcp.resource("resource://boilerplate")
def boilerplate() -> str:
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
    "mondo": "https://rdfportal.org/primary/sparql",
    "ddbj": "https://rdfportal.org/ddbj/sparql",
    "glycosmos": "https://ts.glycosmos.org/sparql",
    "bacdive": "https://rdfportal.org/primary/sparql",
    "mediadive": "https://rdfportal.org/primary/sparql",
    "clinvar": "https://rdfportal.org/ncbi/sparql",
    "ensembl": "https://rdfportal.org/ebi/sparql",
    "nando": "https://rdfportal.org/primary/sparql",
    "pubmed": "https://rdfportal.org/ncbi/sparql",
    "pubtator": "https://rdfportal.org/ncbi/sparql",
    "ncbigene": "https://rdfportal.org/ncbi/sparql",
    "medgen": "https://rdfportal.org/ncbi/sparql",
    "rhea": "https://rdfportal.org/sib/sparql"
}

# The MIE files are used to define the shape expressions for SPARQL queries. 
MIE_DIR = "mie"
MIE_PROMPT="resources/MIE_prompt.md"
RDF_PORTAL_GUIDE="resources/rdf_portal_guide.md"
SPARQL_EXAMPLES="sparql-examples"

RDF_CONFIG_TEMPLATE="rdf-config/template.yaml"

@mcp.tool(name="RDF_Portal_Guide",
            description="A general guideline for using the RDF Portal.")
def rdf_portal_guide() -> str:
    """
    A general guideline for using the RDF Portal.
    Always use this before constructing any SPARQL queries for the database,
    and strictly follow the instructions provided there.

    Returns:
        str: The content of the RDF Portal Guide.
    """
    with open(RDF_PORTAL_GUIDE, "r", encoding="utf-8") as file:
        prompt = file.read()
    return prompt

@mcp.tool(enabled=True, name="Generate_MIE_file", description="Instructions for generating an MIE (Metadata Interoperability Exchange) file")
def generate_MIE_file(
    dbname: Annotated[str, Field(description=f"The name of the database to explore. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    f"""
    Explore a specific RDF database to generate an MIE file for SPARQL queries.

    Args:
        dbname (str): The name of the database to explore. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: The prompt for generating the MIE file for the database.
    """
    with open(MIE_PROMPT, "r", encoding="utf-8") as file:
        mie_prompt = file.read()

    return mie_prompt.replace("__DBNAME__", dbname)


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
    "Then, use `get_graph_list` to explore relevant named graphs, classes, and properties in the database."
 
    )

# --- Tools for RDF Portal --- #

@mcp.tool(enabled=True, name="save_MIE_file", description="Save the provided MIE content to a file named after the database.")
def save_MIE_file(
    dbname: Annotated[str,Field(description=f"database name. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")],
    mie_content: Annotated[str,Field(description="The content of the MIE file to save.", default="#empty MIE file")]
    ) -> str:
    """ 
    Saves the provided MIE content to a file named after the database.

    Returns:
        str: A confirmation message indicating the result of the save operation.
    """
    try:
        # Ensure the MIE directory exists
        os.makedirs(MIE_DIR, exist_ok=True)

        file_path = os.path.join(MIE_DIR, f"{dbname}.yaml")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(mie_content)
        return f"Successfully saved MIE file to {file_path}."
    except (IOError, OSError) as e:
        return f"Error: Could not save MIE file for '{dbname}'. Reason: {e}"

@mcp.tool()
async def get_sparql_endpoints() -> str:
    """ Get the available SPARQL endpoints for RDF Portal. 
    Returns:
        str: A JSON-formatted string containing the available SPARQL endpoints.
    """
    return json.dumps(SPARQL_ENDPOINT)

@mcp.tool(enabled=False)
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
async def execute_sparql_json(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    dbname: Annotated[str, Field(description=f"The name of the database to query. To find the supported databases, use the `get_sparql_endpoints` tool. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
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

async def execute_sparql(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    dbname: Annotated[str, Field(description=f"The name of the database to query. To find the supported databases, use the `get_sparql_endpoints` tool. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    """ Execute a SPARQL query on RDF Portal. 
    Args:
        sparql_query (str): The SPARQL query to execute.
        dbname (str): The name of the database to query. To find the supported databases, use the `get_sparql_endpoints` tool.
    Returns:
        dict: The results of the SPARQL query in CSV.
    """

    if dbname not in SPARQL_ENDPOINT:
        raise ValueError(f"Unknown database: {dbname}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPARQL_ENDPOINT[dbname], data={"query": sparql_query}, headers={"Accept": "text/csv"}
        )
    response.raise_for_status()
    return response.text

@mcp.tool(
        enabled=True,
        name="run_sparql",
        description="Run a SPARQL query on a specific RDF database."
)
async def run_sparql(
    sparql_query: Annotated[str, Field(description="The SPARQL query to execute")],
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")],
) -> str:
    """
    Run a SPARQL query on a specific RDF database. Use `describe_rdf_schema()` to understand the RDF graph structure of the database.

    Args:
        sparql_query (str): The SPARQL query to execute.
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT_KEYS)}.

    Returns:
        str: CSV-formatted results of the SPARQL query.
    """
    return await execute_sparql(sparql_query, dbname)

# --- Tools for exploring RDF databases ---
@mcp.tool(
        enabled=False,
        name="get_class_list",
        description="Get a list of classes in the RDF database that match the given URI."
)
async def get_class_list(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")],
    uri: Annotated[str, Field(description="The URI to match classes. `http://...`")]
) -> str:
    f"""
    Get a list of classes in the RDF database that match the given URI.

    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.
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
        enabled=False,
        name="get_property_list",
        description="Get a list of properties in the RDF database that match the given URI."
)
async def get_property_list(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")],
    uri: Annotated[str, Field(description="The URI to match properties. `http://...`")]
) -> str:
    f"""
    Get a list of properties in the RDF database that match the given URI.

    Args:
        dbname (str): The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.
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
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
    ) -> str:
    f"""
    Get a list of named graphs in a specific RDF database.

    Args:
        dbname (str): The name of the database for which to retrieve the named graphs. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: CSV-formatted list of named graphs.
    """
    sparql_query = '''
SELECT DISTINCT ?graph WHERE {
  GRAPH ?graph {
    ?s ?p ?o .
  }
}'''
    return await execute_sparql(sparql_query, dbname)

@mcp.tool(enabled=True)
async def get_shex(
    dbname: Annotated[str, Field(description=f"database name. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    """
    Get the ShEx schema for a specific RDF database.

    Args:
        dbname(str): The name of the database for which to retrieve the ShEx schema. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.

    Returns:
        str: The ShEx schema in ShEx format.
    """
    shex_file = "shex/" + dbname + ".shex"
    if not os.path.exists(shex_file):
        return f"Error: The shex file for '{dbname}' was not found."
    try:
        with open(shex_file, "r", encoding="utf-8") as file:
            content = file.read()
            return content
    except Exception as e:
        return f"Error reading shex file for '{dbname}': {e}"

@mcp.tool(
        enabled=True,
        name="get_MIE_file",
        description="Get the MIE file containing the ShEx schema, RDF and SPARQL examples of a specific RDF database. Use this before constructing any SPARQL queries for the database."
)
async def get_MIE_file(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
    ) -> str:
    f"""
    Get the MIE file containing the ShEx schema, RDF and SPARQL examples of a specific RDF database in YAML format, which can be used as a hint to build SPARQL queries.

    Args:
        dbname (str): The name of the database for which to retrieve the shape expression. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}."

    Returns:
        str: The MIE file containing the RDF schema information in YAML format.
    """
    mie_file = MIE_DIR + "/" + dbname + ".yaml"
    drop_keys = [] 
#    drop_keys += ["data_statistics", "architectural_notes"]
#    drop_keys += ["validation_notes"]
    if not os.path.exists(mie_file):
        return f"Error: The MIE file for '{dbname}' was not found."
    try:
        with open(mie_file, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            content2 = {}
            if isinstance(content, dict):
                for key, value in content.items():
                    if key not in drop_keys:
                        content2[key] = value
                yaml_dump = yaml.dump(content2, sort_keys=False)
            else:
                # If not a dictionary, just dump the original content
                yaml_dump = yaml.dump(content, sort_keys=False)
            
            response_text = f"""Content-type: application/yaml; charset=utf-8
{yaml_dump}"""
            return response_text
    except Exception as e:
        return f"Error reading MIE file for '{dbname}': {e}"

@mcp.tool(
    enabled=True, 
    name="list_databases",
    description="List available databases and their descriptions."
)
def list_databases() -> List[Dict[str, Any]]:
    """
    Reads all YAML files in a given directory and extracts the title and
    description from the 'schema_info' section.

    Returns:
        A list of dictionaries, each containing schema info for a file.
    """
    resources_dir = MIE_DIR
    if not os.path.isdir(resources_dir):
        print(f"Error: Directory '{resources_dir}' not found.", file=sys.stderr)
        return []

    all_schemas_info = []
    for db_name in sorted(SPARQL_ENDPOINT.keys()):
        filename = db_name + ".yaml"
        print(f"##### Processing file: {filename}", file=sys.stderr)
        file_path = os.path.join(resources_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise yaml.YAMLError("YAML file is not a dictionary.")
            
            schema_info = data.get("schema_info")
            if not isinstance(schema_info, dict):
                raise yaml.YAMLError("'schema_info' section not found or not a dictionary.")

            title = schema_info.get("title")
            description = schema_info.get("description")

            all_schemas_info.append({
                "database": db_name,
                "title": title or "No title found.",
                "description": description or "No description found.",
            })

        except yaml.YAMLError as e:
            all_schemas_info.append(
                {
                    "database": db_name,
                    "title": "No title found.",
                    "description": f"Error processing YAML file: {e}",
                })
        except (IOError, OSError) as e:
            all_schemas_info.append(
                {
                    "database": db_name,
                    "title": "No title found.",
                    "description": f"Error reading file: {e}",
                })
    return all_schemas_info

@mcp.tool(
        enabled=True,
        description="Get an example SPARQL query for a specific RDF database.",
        name="get_sparql_example"
)
def get_sparql_example(
    dbname: Annotated[str, Field(description=f"The name of the database to query. Supported values are {', '.join(SPARQL_ENDPOINT.keys())}.")]
) -> str:
    """
    Read the file in SPARQL_EXAMPLES/{dbname}.rq and return the content.

    Args:
        dbname (str): The name of the database for which to retrieve the SPARQL example.

    Returns:
        str: The content of the SPARQL example file, or an error message if not found.
    """
    example_file = os.path.join(SPARQL_EXAMPLES, f"{dbname}.rq")
    if not os.path.exists(example_file):
        return f"Error: The SPARQL example file for '{dbname}' was not found at '{example_file}'."
    try:
        with open(example_file, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading SPARQL example file for '{dbname}': {e}"

if __name__ == "__main__":
    mcp.run()