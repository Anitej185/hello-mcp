# from mcp.server.fastmcp import FastMCP
# from pydantic import Field

# mcp = FastMCP(name="Hello MCP Server")

# @mcp.tool(
#     title="Welcome a user",
#     description="Return a friendly welcome message for the user.",
# )
# def welcome(name: str = Field(description="Name of the user")) -> str:
#     return f"Welcome {name} from this amazing application!"

# if __name__ == "__main__":
#     # letting FastMCP auto-pick a port and announce it
#     mcp.run(transport="stdio")

from mcp.server.fastmcp import FastMCP
from pydantic import Field

# keeping it simple; let FastMCP manage the HTTP server
mcp = FastMCP(name="Hello MCP Server", stateless_http=True)

@mcp.tool(
    title="Welcome a user",
    description="Return a friendly welcome message for the user.",
)
def welcome(name: str = Field(description="Name of the user")) -> str:
    return f"Welcome {name} from this amazing application!"

# running on import so the platform/Lambda boots the server automatically
mcp.run(transport="streamable-http")
