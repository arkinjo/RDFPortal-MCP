import sys
from fastmcp import FastMCP
import httpx

print("Starting Wikidata API MCP server...", file=sys.stderr)
# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://wikidata.org/w/rest.php/wikibase/v1")

# Load your OpenAPI spec 
# Currentyly, this doesn't work!
openapi_spec = httpx.get("https://wikidata.org/w/rest.php/wikibase/v1/openapi.json").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Wikidata API Server"
)

if __name__ == "__main__":
    mcp.run()

