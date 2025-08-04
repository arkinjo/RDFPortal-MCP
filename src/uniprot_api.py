import sys
from fastmcp import FastMCP
import httpx

print("Starting UniProt API MCP server...", file=sys.stderr)
# Create an HTTP client for your API
client = httpx.AsyncClient(base_url="https://rest.uniprot.org")

# Load your OpenAPI spec 
openapi_spec = httpx.get("https://rest.uniprot.org/uniprotkb/api/docs").json()

# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="UniProt API Server"
)

if __name__ == "__main__":
    mcp.run()

