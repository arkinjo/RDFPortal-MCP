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



# DB: Glycosmos
@mcp.tool(enabled=True)
async def glycoepitope_epitope_gtc(epitopeID: str) -> str:
    """
    Retrieve GlyTouCan IDs associated with a given glycoepitope ID.

    Args:
        epitopeID (str): 
            The glycoepitope ID to search to retrieve the corresponding GlyTouCan ID. This should be a valid glycoepitope ID string (e.g., EP####).

    Returns:
        glytoucanID (str): The GlyTouCan ID associated with the given glycoepitope."
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/glycoepitope_epitope_gtc"
    params = {
        "epitopeID": epitopeID
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return json.dumps(data)


@mcp.tool(enabled=True)
async def gtc_image(accession: str, 
                    style: str = "extended", 
                    notation: str = "snfg", 
                    format: str = "svg", 
                    graph: str = "http://rdf.glytoucan.org/image"
                    ) -> str:
    """
    Get image data from GlyTouCan

    Args:
        accession (str): 
            The GlyTouCan accession number that uniquely identifies a glycan structure.
            Example: "G39023AU"
        
        style (str, optional): 
            The image style to use. 
            Default is "extended".
            Options: "extended".
        
        notation (str, optional): 
            Symbol notation system used to draw or describe the glycan.
            Default is "snfg".
            Options include: "cfg", "cfg_bw", "cfg_uoxf", "uoxf", "uoxf_color", "iupac", "snfg".
        
        format (str, optional): 
            The output format of the image.
            Default is "svg".
            Options: "png" or "svg".
        
        graph (str, optional): 
            The RDF graph URI to use as the data source.
            Default is "http://rdf.glytoucan.org/image".

    Returns:
        format: json
        fields:
            - image_tag: Ready-to-use `<img>` HTML tag string
            - image_base64: Base64-encoded string of the image
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/gtc_image"
    params = {
        "accession": accession,
        "style": style,
        "notation": notation,
        "format": format,
        "graph": graph
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    return response.text


@mcp.tool(enabled=True)
async def gtc_external_id(accNum: str) -> str:
    """
    Retrieve external database cross-references for a given GlyTouCan accession number.  
    Returns mappings to partner databases (KEGG, BCSDB, GlyGen, UniCarb-DB, GlycoEpitope, GlycoChemExplorer, JCGGDB AIST), including database-specific IDs, URLs, and descriptions.

    Args:
        accNum (str): 
            The GlyTouCan ID (also called as accession number) to find the external resources linked the ID.

    Returns:
        format: json
        fields:
            - entry_label: Label of the external resource (e.g., KEGG GLYCAN, GlyGen)
            - id: External identifier from the partner database
            - url: Direct URL to the partner database entry
            - from: Source database name
            - description: Description of the partner database
            - partnerurl: Homepage of the partner database
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/gtc_external_id"
    params = {
        "accNum": accNum
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return json.dumps(data)


@mcp.tool(enabled=True) # TODO: which gene id?
async def gene_and_organism_annotation(tax_id: str, gene_id: str) -> str:
    """
    Map a gene in a given species (by NCBI Taxonomy ID and gene symbol) to UniProt IDs, 
    protein names, synonyms, and lineage information. Useful for annotating genes across species.

    Args:
        - tax_id (str): NCBI Taxonomy ID (e.g., "9606" for human).
        - gene_id (str): Gene symbol or identifier (e.g., "BRCA1").

    Returns:
        format: json
        fields:
            - tg: TogoGenome gene URI
            - up: UniProt protein URIs
            - rs: RefSeq identifiers
            - protein_name: Common protein name
            - synonym_name: Gene synonyms
            - recommended_name: UniProt recommended protein name
            - ec_name: EC enzyme classification numbers
            - alternative_name: Alternate names
            - lineage: Full taxonomic lineage
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/gene_and_organism_annotation"
    params = {
        "tax_id": tax_id,
        "gene_id": gene_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return json.dumps(data)


@mcp.tool(enabled=True)
async def uniprot_aa_seq(up_id: str) -> str:
    """
    Retrieve the amino acid sequence and length of a glycoprotein given its UniProt accession ID.
    Input is a UniProt ID (e.g., "P02873"). Returns the raw amino acid sequence and its length.

    Args:
        up_id: UniProt protein accession ID (e.g., "P02873").

    Returns:
        format: json
        fields:
            - aa_seq: full amino acid sequence string
            - length: length of the sequence in amino acids
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/uniprot_aa_seq"
    params = {
        "up_id": up_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return json.dumps(data)


@mcp.tool(enabled=True)
async def gtcId2Seq(id: str) -> str:
    """
    Retrieve glycan sequences from GlyTouCan by accession number.
      Supports both WURCS and GlycoCT sequence formats. Input is a GlyTouCan ID
      (e.g., "G95616YE"). Returns sequence data if available.

    Args:
        id: GlyTouCan accession number (e.g., "G95616YE").

    Returns:
        format: json
        fields:
            - GlyTouCan: the accession number provided
            - WURCS: WURCS sequence string (if available)
            - GlycoCT: GlycoCT sequence string (if available)
    """
    url = f"https://sparqlist.glycosmos.org/sparqlist/api/gtcId2Seq"
    params = {
        "id": id
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return json.dumps(data)


if __name__ == "__main__":
    mcp.run()
