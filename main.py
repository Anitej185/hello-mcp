import os
from fastmcp import FastMCP
from pydantic import Field

# Get port from environment variable or use default
port = int(os.environ.get("PORT", 8080))

mcp = FastMCP(
    name="Hello MCP Server",
    stateless_http=True,
    debug=False,
)

@mcp.tool(
    title="Welcome a user",
    description="Return a friendly welcome message for the user.",
)
def welcome(
    name: str = Field(description="Name of the user")
) -> str:
    return f"Welcome {name} from this amazing application!"

@mcp.tool(
    title="Get server info",
    description="Get information about the MCP server.",
)
def server_info() -> str:
    return f"MCP Server running with streamable-http transport"

# IMPORTANT: no __main__ guard for deployment; start on import so Lambda boots the server automatically
mcp.run(transport="streamable-http")
