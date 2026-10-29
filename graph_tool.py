from langchain.tools import tool
from neo4j_db import get_driver

driver = get_driver()


@tool
def employees_in_department(department: str):
    """
    Find all employees in a department.
    """

    query = """
    MATCH (e:Employee)-[:WORKS_IN]->(d:Department)
    WHERE toLower(d.name) = toLower($department)
    RETURN e.name AS employee
    ORDER BY e.name
    """

    with driver.session() as session:
        result = session.run(query, department=department)
        employees = [record["employee"] for record in result]

    if not employees:
        return f"No employees found in {department}."

    return "\n".join(employees)
@tool
def employees_with_skill(skill: str, min_experience: int = None):
    """
    Find employees with a given skill.
    Optionally filter by minimum years of experience.
    """

    query = """
    MATCH (e:Employee)-[:HAS_SKILL]->(s:Skill)
    WHERE toLower(s.name) = toLower($skill)
    """

    if min_experience is not None:
        query += """
        AND e.experience >= $min_experience
        """

    query += """
    RETURN e.name AS employee,
           e.experience AS experience
    ORDER BY e.experience DESC
    """

    with driver.session() as session:
        result = session.run(
            query,
            skill=skill,
            min_experience=min_experience,
        )

        employees = [
            f"{record['employee']} ({record['experience']} years)"
            for record in result
        ]

    if not employees:
        return f"No employees found with skill '{skill}'."

    return "\n".join(employees)