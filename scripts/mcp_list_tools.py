import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent


async def main():
    # Launch the Dagster MCP server via uvx (same as mcp.json)
    server_params = StdioServerParameters(
        command="uvx",
        args=[
            "--from",
            "dagster-dg[mcp]",
            "--with",
            "dagster",
            "--with",
            "dagster-webserver",
            "dg",
            "--path",
            ".",
            "mcp",
            "serve",
        ],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tool_list = await session.list_tools()
            tools = tool_list.tools
            print("Tools:", [t.name for t in tools])

            # Try a simple tool invoking: prefer defs/components listing if available
            target_tool = None
            for name in [
                "list_dagster_definitions",
                "list_defs",
                "list-defs",
                "defs.list",
                "list_components",
                "list-components",
                "components.list",
            ]:
                if any(t.name == name for t in tools):
                    target_tool = name
                    break

            if target_tool:
                print(f"Invoking tool: {target_tool}")
                res = await session.call_tool(target_tool, {"project_path": "packages/confradar"})
                # Print text-like content
                texts = []
                for c in res.content:
                    if isinstance(c, TextContent):
                        texts.append(c.text)
                if texts:
                    print("Result:\n" + "\n".join(texts))
                else:
                    print("Got non-text content:", res.content)
            else:
                print("No explicit defs/components tool found; server is reachable and tools are listed.")


if __name__ == "__main__":
    asyncio.run(main())
