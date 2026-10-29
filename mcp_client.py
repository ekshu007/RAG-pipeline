import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:\n")

            for tool in tools.tools:
                print(tool.name)
                print(tool.description)
                print("-" * 40)
            print("\n Calling leave balance...\n")
            result=await session.call_tool("leave_balance",
                                           arguments={"employee_id":101}
                                           )
            print(result)
            print("\nCalling employee details\n")
            result=await session.call_tool("employee_details",arguments={'employee_id':101})
            print(result)

            result=await session.call_tool("announcement",arguments={
                "topic":"Office will remain closed on Friday for maintainance"
            })
            print(result)

if __name__ == "__main__":
    asyncio.run(main())