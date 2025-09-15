import httpx
from fastmcp import FastMCP
from typing import List, Dict, Annotated
from pydantic import Field
import json


mcp = FastMCP("TogoMCP Support API Tools")

######################################
#####　Database-specific tools ########
######################################
# DB: UniProt
@mcp.tool(enabled=True)
async def search_uniprot_entity(query: str, limit: int = 20) -> str:
    """
    Search for a UniProt entity ID by query.

    Args:
        query (str): The query to search for. The query should be unambiguous enough to uniquely identify the entity.
        limit (int): The maximum number of results to return. Default is 20.

    Returns:
        str: The UniProt protein entity ID corresponding to the given query."
    """
    url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "fields": "accession,protein_name,gene_names,organism_name",
        "format": "json",
        "size": limit 
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract just the primary accession ID from each result
    uniprot_ids = [entry.get("primaryAccession") for entry in data.get("results", []) if "primaryAccession" in entry]
    return json.dumps(uniprot_ids)

# DB: ChEMBL
async def search_chembl_generic(entity_type: str, query: str, limit: int = 20) -> dict:
    """
    Search for ChEMBL ID by query.

    Args:
        entity_type (str): The type of entity to search for.
        query (str): The query string to search for.
        limit (int): The maximum number of results to return.

    Returns:
        A dictionary parsed from the JSON response.
    """
    url = f"https://www.ebi.ac.uk/chembl/api/data/{entity_type}/search.json"
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.json()


@mcp.tool()
async def search_chembl_id_lookup(
    query: Annotated[str, Field(description="The query string to search for.")],
    limit: Annotated[int, Field(description="The maximum number of results to return.")] = 20
    ) -> dict:
    """
    Search for ChEMBL ID by query.

    Returns:
        str: A JSON-formatted string containing the search results.
    """
    bulk = await search_chembl_generic("chembl_id_lookup", query, limit)
    total_count = bulk.get("page_meta", {}).get("total_count", 0)
    parsed_results = []
    for result in bulk.get("chembl_id_lookups", []):
        parsed_results.append({
            "chembl_id": result.get("chembl_id"),
            "entity_type": result.get("entity_type"),
            "score": result.get("score")})

    return {"total_count": total_count, "results": parsed_results}

@mcp.tool()
async def search_chembl_target(query: str, limit: int = 20) -> dict:
    """
    Search for ChEMBL target by query.
    """
    bulk = await search_chembl_generic("target", query, limit)
    total_count = bulk.get("page_meta", {}).get("total_count", 0)

    parsed_results = []
    for target in bulk.get("targets", []):
        parsed_results.append({
            "chembl_id": target.get("target_chembl_id"),
            "name": target.get("pref_name"),
            "organism": target.get("organism"),
            "type": target.get("target_type"),
            "score": target.get("score")
        })

    return {"total_count": total_count, "results": parsed_results}


@mcp.tool()
async def search_chembl_molecule(query: str, limit: int = 20) -> dict:
    """
    Search for ChEMBL molecule by query.
    """
    bulk = await search_chembl_generic("molecule", query, limit)
    total_count = bulk.get("page_meta", {}).get("total_count", 0)
    parsed_results = []
    for molecule in bulk.get("molecules", []):
        parsed_results.append({
            "chembl_id": molecule.get("molecule_chembl_id"),
            "name": molecule.get("pref_name"),
            "score": molecule.get("score")
        })

    return {"total_count": total_count, "results": parsed_results}

@mcp.tool(enabled=False)
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


# DB: PubChem
@mcp.tool()
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

@mcp.tool()
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

# DB: PDB
@mcp.tool()
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
    # Parse the response as JSON
    total_results = response.json().get("total", 0)
    result_list = [{entry[0]: entry[1]} for entry in response.json().get("results", [])[:limit]]
    response_dict = {"total": total_results, "results": result_list}
    return json.dumps(response_dict)

@mcp.tool(enabled=False)
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

# DB: MeSH
@mcp.tool()
async def search_mesh_entity(query: str, limit: int = 10) -> str:
    """
    Search for MeSH ID by query.

    Args:
        query (str): The query string to search for.
        limit (int): The maximum number of results to return. Default is 10.

    Returns:
        str: A JSON-formatted string containing the search results.
    """
    url = "https://id.nlm.nih.gov/mesh/lookup/term"
    params = {"label": query,
              "match": "contains",
              "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.text

# DB: Wikidata
WIKIDATA_URL = "https://www.wikidata.org/w/api.php"
HEADER = {"Accept": "application/json", "User-Agent": "foobar"}


async def search_wikidata(query: str, is_entity: bool = True) -> str:
    """
    Search for a Wikidata item or property ID by its query.
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 0 if is_entity else 120,
        "srlimit": 1,  # TODO: add a parameter to limit the number of results?
        "srqiprofile": "classic_noboostlinks" if is_entity else "classic",
        "srwhat": "text",
        "format": "json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WIKIDATA_URL, headers=HEADER, params=params)
    response.raise_for_status()
    try:
        title = response.json()["query"]["search"][0]["title"]
        title = title.split(":")[-1]
        return title
    except KeyError:
        return "No results found. Consider changing the search term."


@mcp.tool(
    name="search_wikidata_entity",
    description="Search for a Wikidata entity ID by its query. The query should be unambiguous enough to uniquely identify the entity.",
 )
async def search_wikidata_entity(query: str) -> str:
    """
    Search for a Wikidata entity ID by its query.

    Args:
        query (str): The query to search for. The query should be unambiguous enough to uniquely identify the entity.

    Returns:
        str: The Wikidata entity ID corresponding to the given query."
    """
    return await search_wikidata(query, is_entity=True)


@mcp.tool()
async def search_wikidata_property(query: str) -> str:
    """
    Search for a Wikidata property ID by its query.

    Args:
        query (str): The query to search for. The query should be unambiguous enough to uniquely identify the property.

    Returns:
        str: The Wikidata property ID corresponding to the given query."
    """
    return await search_wikidata(query, is_entity=False)


@mcp.tool()
async def get_wikidata_properties(entity_id: str) -> List[str]:
    """
    Get the properties associated with a given Wikidata entity ID.

    Args:
        entity_id (str): The entity ID to retrieve properties for. This should be a valid Wikidata entity ID.

    Returns:
        list: A list of property IDs associated with the given entity ID. If no properties are found, an empty list is returned.
    """
    params = {
        "action": "wbgetentities",
        "ids": entity_id,
        "props": "claims",
        "format": "json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WIKIDATA_URL, headers=HEADER, params=params)
    response.raise_for_status()
    data = response.json()
    return list(data.get("entities", {}).get(entity_id, {}).get("claims", {}).keys())

@mcp.tool()
async def get_wikidata_metadata(entity_id: str, language: str = "en") -> Dict[str, str]:
    """
    Retrieve the English label and description for a given Wikidata entity ID.

    Args:
        entity_id (str): The entity ID to retrieve metadata for.
        language (str): The language code for the label and description (default is "en"). Use ISO 639-1 codes.

    Returns:
        dict: A dictionary containing the label and description of the entity, if available.
    """
    params = {
        "action": "wbgetentities",
        "ids": entity_id,
        "props": "labels|descriptions",
        "languages": language,  # specify the desired language
        "format": "json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(WIKIDATA_URL, params=params)
    response.raise_for_status()
    data = response.json()
    entity_data = data.get("entities", {}).get(entity_id, {})
    label = (
        entity_data.get("labels", {}).get(language, {}).get("value", "No label found")
    )
    descriptions = (
        entity_data.get("descriptions", {})
        .get(language, {})
        .get("value", "No label found")
    )
    return {"Label": label, "Descriptions": descriptions}

if __name__ == "__main__":
    mcp.run()
