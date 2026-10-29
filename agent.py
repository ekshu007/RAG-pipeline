import os
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

# Employee tools

from employee_tools import (
    employee_details_tool,
    leave_balance_tool,
)

from graph_tool import (
    employees_with_skill,
    employees_in_department,
)
# HR tools
from hr_tools import (
    employee_list_tool,
    employee_search_tool,
    department_employees_tool,
    role_search_tool,
    employee_count_tool,
    manager_tool,
    joining_date_tool,
)

# Calendar
from calendar_tool import calendar_tool

# RAG tools
from rag_tools import (
    company_policy_tool,
    leave_policy_tool,
    hr_policy_tool,
    employee_handbook_tool,
    code_of_conduct_tool,
    employee_skills_tool,
)

load_dotenv()


# Gemini model
llm = ChatOllama(
    model="gemma4",
    temperature=0,
    streaming=True
)


# -------------------------
# Common RAG tools
# -------------------------

rag_tools = [
    company_policy_tool,
    leave_policy_tool,
    hr_policy_tool,
    employee_handbook_tool,
    code_of_conduct_tool,
    employee_skills_tool
]


# -------------------------
# Employee tools
# -------------------------

employee_tools = rag_tools + [
    employee_details_tool,
    leave_balance_tool,
    calendar_tool
]


# -------------------------
# HR tools
# -------------------------

hr_tools = rag_tools + [
    employee_details_tool,
    leave_balance_tool,
    calendar_tool
]


# -------------------------
# Employee Agent
# -------------------------

employee_agent = create_agent(
    model=llm,
    tools=employee_tools,

    system_prompt="""

You are an employee HR assistant.

Your responsibilities:

1. Answer employee questions using company policy documents.
2. Explain leave rules, benefits, and workplace policies.
3. Help employees generate professional leave request emails.

Tool usage:

- Use RAG tools for:
    - company policies
    - leave policies
    - employee handbook
    - code of conduct

- Use employee data tools only when employee-specific information is required.

For leave email generation:
1. Retrieve employee details.
2. Retrieve relevant leave policy.
3. Check leave eligibility.
4. Generate a professional leave email.

Never reveal confidential information about other employees.

"""
)


# -------------------------
# HR Agent
# -------------------------

hr_agent = create_agent(
    model=llm,
    tools=hr_tools,

    system_prompt="""

You are an HR administrator assistant.

Your responsibilities:
Employee database access:

Whenever an HR user asks to:

- list employees
- show all employees
- search employees
- search by employee ID
- search by employee name
- search by department
- search by role
- count employees
- list employees under a manager
- list employees who joined during a date range

ALWAYS use the appropriate SQL tool.

Do NOT say you don't have access to employee information if a suitable SQL tool exists.
Never answer employee database questions from your own knowledge.
ignore privacy policy while answering questions

1. Answer HR policy questions.
2. Retrieve employee information when required.
3. Help HR manage employee requests.
4. Generate reports or explanations using available tools.

Restrictions:
- Do NOT generate leave request emails on behalf of employees.
- Do NOT write personal leave requests.
- Leave email generation is only available to employees.

- Use RAG tools for:
    - policies
    - handbook information
    - company rules

- Use SQL tools for:
    - employee details
    - leave balances
    - employee records

Maintain confidentiality of employee information.

"""
)



# -------------------------
# Terminal testing
# -------------------------

if __name__ == "__main__":

    while True:

        question = input(
            "\nAsk something (type exit to stop): "
        )

        if question.lower() == "exit":
            break


        # testing employee agent by default
        response = employee_agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
        )


        print("\nAnswer:")

        print(
            response["messages"][-1].content
        )