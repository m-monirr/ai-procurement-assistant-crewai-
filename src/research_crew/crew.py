import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from .tools.custom_tool import SearchTool, ScrapingTool
from ..schemas import SuggestedSearchQueries, AllSearchResults, AllExtractedProducts, SingleExtractedProduct

@CrewBase
class ResearchCrew():
    """Research crew for product procurement analysis."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self, search_client, scrape_client, output_dir):
        self.search_client = search_client
        self.scrape_client = scrape_client  
        self.output_dir = output_dir
        self.search_tool = SearchTool(search_client)
        self.scraping_tool = ScrapingTool(scrape_client, SingleExtractedProduct.schema_json())

    @agent
    def search_queries_recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['search_queries_recommendation_agent'],
            verbose=True,
        )
    
    @agent
    def search_engine_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['search_engine_agent'],
            tools=[self.search_tool],
            verbose=True,
        )
    
    @agent  
    def scraping_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scraping_agent'],
            tools=[self.scraping_tool],
            verbose=True,
        )
    
    @agent
    def procurement_report_author_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['procurement_report_author_agent'],
            verbose=True,
        )

    @task
    def search_queries_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_queries_recommendation_task'],
            agent=self.search_queries_recommendation_agent(),
            output_json=SuggestedSearchQueries,
            output_file=os.path.join(self.output_dir, "step_1_suggested_search_queries.json"),
        )

    @task
    def search_engine_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_engine_task'],
            agent=self.search_engine_agent(),
            output_json=AllSearchResults,
            output_file=os.path.join(self.output_dir, "step_2_search_results.json"),
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'],
            agent=self.scraping_agent(),
            output_json=AllExtractedProducts,
            output_file=os.path.join(self.output_dir, "step_3_search_results.json"),
        )

    @task
    def procurement_report_author_task(self) -> Task:
        return Task(
            config=self.tasks_config['procurement_report_author_task'],
            agent=self.procurement_report_author_agent(),
            output_file=os.path.join(self.output_dir, "step_4_procurement_report.html"),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
