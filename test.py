from graph_tool import employees_with_skill

print(
    employees_with_skill.invoke(
        {
            "skill": "Python"
        }
    )
)