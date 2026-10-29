from dotenv import load_dotenv
load_dotenv()
from hr_tools import leave_balance_tool
from hr_tools import employee_details_tool
from mcp.server.fastmcp import FastMCP
from services.announcement_service import generate_announcement
mcp=FastMCP("HR agent")
@mcp.tool()
def leave_balance(employee_id: int):
    """Get an employee's leave balance"""
    return leave_balance_tool.invoke({"employee_id":employee_id})


@mcp.tool()
def employee_details(employee_id:int):
    """Get employee details"""
    return employee_details_tool.invoke({"employee_id":employee_id})
if __name__=="__main__":
    print("Starting MCP server")
    mcp.run()

@mcp.tool()
def announcement(topic:str):
    """Generatea professional HR announcement"""
    return generate_announcement(topic)