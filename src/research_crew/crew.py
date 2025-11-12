import os
import sys
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Add root directory to path for schemas import
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from schemas import SuggestedSearchQueries, AllSearchResults, AllExtractedProducts, SingleExtractedProduct
from .tools.custom_tool import SearchTool, ScrapingTool

@CrewBase
class ResearchCrew():
    """Research crew for product procurement analysis."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self, search_client, scrape_client, output_dir, llm):
        # Store clients and output directory
        self._search_client = search_client
        self._scrape_client = scrape_client  
        self._output_dir = output_dir
        
        # Initialize tools
        self._search_tool = SearchTool(search_client)
        self._scraping_tool = ScrapingTool(scrape_client, SingleExtractedProduct.schema_json())

        # Store the LLM for agents
        self._llm = llm

    @agent
    def search_queries_recommendation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['search_queries_recommendation_agent'],
            llm=self._llm,
            verbose=True,
        )
    
    @agent
    def search_engine_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['search_engine_agent'],
            llm=self._llm,
            tools=[self._search_tool],
            verbose=True,
        )
    
    @agent  
    def scraping_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scraping_agent'],
            llm=self._llm,
            tools=[self._scraping_tool],
            verbose=True,
        )
    
    @agent
    def procurement_report_author_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['procurement_report_author_agent'],
            llm=self._llm,
            verbose=True,
        )

    @task
    def search_queries_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_queries_recommendation_task'],
            agent=self.search_queries_recommendation_agent(),
            output_file=os.path.join(self._output_dir, "step_1_suggested_search_queries.json"),
        )

    @task
    def search_engine_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_engine_task'],
            agent=self.search_engine_agent(),
            output_file=os.path.join(self._output_dir, "step_2_search_results.json"),
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'],
            agent=self.scraping_agent(),
            output_file=os.path.join(self._output_dir, "step_3_search_results.json"),
        )

    @task
    def procurement_report_author_task(self) -> Task:
        return Task(
            config=self.tasks_config['procurement_report_author_task'],
            agent=self.procurement_report_author_agent(),
            output_file=os.path.join(self._output_dir, "step_4_procurement_report.html"),
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
