from crewai.tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input schema for SearchTool."""
    query: str = Field(..., description="The search query to execute")

class ScrapingInput(BaseModel):
    """Input schema for ScrapingTool."""
    page_url: str = Field(..., description="The URL of the webpage to scrape")

class SearchTool(BaseTool):
    name: str = "Search Engine Tool"
    description: str = "Useful for search-based queries. Use this to find current information about any query related pages using a search engine"
    args_schema: Type[BaseModel] = SearchInput
    
    def __init__(self, search_client, **kwargs):
        super().__init__(**kwargs)
        # Store client in a private attribute that won't conflict with pydantic
        self._search_client = search_client
    
    def _run(self, query: str) -> str:
        """Execute the search query using Tavily client."""
        try:
            results = self._search_client.search(query)
            return str(results)
        except Exception as e:
            return f"Error during search: {str(e)}"

class ScrapingTool(BaseTool):
    name: str = "Web Scraping Tool"
    description: str = "An AI Tool to help an agent to scrape a web page and extract product information"
    args_schema: Type[BaseModel] = ScrapingInput
    
    def __init__(self, scrape_client, schema_json, **kwargs):
        super().__init__(**kwargs)
        # Store clients in private attributes
        self._scrape_client = scrape_client
        self._schema_json = schema_json
    
    def _run(self, page_url: str) -> str:
        """Extract product details from the given webpage URL."""
        try:
            details = self._scrape_client.smartscraper(
                website_url=page_url,
                user_prompt=f"Extract ```json\n{self._schema_json}\n``` From the web page"
            )
            
            return str({
                "page_url": page_url,
                "details": details
            })
        except Exception as e:
            return f"Error during scraping: {str(e)}"
