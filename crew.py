from crewai import Crew, Process

def create_crew(agents, tasks, company_context):
    # Create crew without knowledge sources for now
    hope_crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        # knowledge_sources=[company_context]  # Commented out to avoid embedding issues
    )
    return hope_crew
