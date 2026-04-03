from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def greet(name: str) -> str:
    """Say hello to someone by name."""
    return f"Hello, {name}!"

# Add more tools with the @mcp.tool() decorator

if __name__ == "__main__":
    mcp.run(transport="stdio")