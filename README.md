# RDFPortal-MCP
This MCP server executes SPARQL queries against various RDF databases provided at the [RDF Portal](https://rdfportal.org/). 

Additional functionalities are also provided that interact with a few REST APIs at various sites.

## Installation
- Python (>= 3.11)
- [uv](https://docs.astral.sh/uv/) package manager

### Install uv (if not yet installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows... I have no idea, sorry.
```
### Install RDFPortal-MCP server
```bash
# Clone the repository
git clone https://github.com/arkinjo/RDFPortal-MCP.git
cd RDFPortal-MCP

# Install dependencies
uv sync

```

## Configuration
### Claude Desktop Configuration
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
```json
{
    "mcpServers": {
        "rdfportal": {
            "command": "/Users/arkinjo/.local/bin/uv",
            "args":[
                "--directory",
                "/Users/arkinjo/work/GitHub/RDFPortal-MCP",
                "run",
                "src/server.py"
            ]
        },
        "api_tools": {
            "command": "/Users/arkinjo/.local/bin/uv",
            "args": [
                "--directory",
                "/Users/arkinjo/work/GitHub/RDFPortal-MCP",
                "run",
                "src/api_tools.py"
            ]
        }
    }
}
```
Here, "rdfportal" is the main MCP server for RDFPortal, whereas "api_tools" is an additional (optional) MCP server providing REST APIs.