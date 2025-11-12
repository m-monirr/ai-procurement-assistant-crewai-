import os
from crewai import Agent, Task
from crewai.tools import tool
from schemas import SuggestedSearchQueries, AllSearchResults, AllExtractedProducts, SingleExtractedProduct

def create_search_tool(search_client):
    @tool
    def search_engine_tool(query: str):
        """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
        return search_client.search(query)
    return search_engine_tool

def create_scraping_tool(scrape_client):
    @tool
    def web_scraping_tool(page_url: str):
        """
        An AI Tool to help an agent to scrape a web page
        
        Example:
        web_scraping_tool(
            page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
        )
        """
        details = scrape_client.smartscraper(
            website_url=page_url,
            user_prompt="Extract ```json\n" + SingleExtractedProduct.schema_json() + "```\n From the web page"
        )
        
        return {
            "page_url": page_url,
            "details": details
        }
    return web_scraping_tool

def create_agents_and_tasks(basic_llm, output_dir, search_client, scrape_client):
    # Create tools with clients
    search_tool = create_search_tool(search_client)
    scraping_tool = create_scraping_tool(scrape_client)
    
    search_queries_recommendation_agent = Agent(
        role="Search Queries Recommendation Agent",
        goal="\n".join([
                    "To provide a list of suggested search queries to be passed to the search engine.",
                    "The queries must be varied and looking for specific items."
                ]),
        backstory="The agent is designed to help in looking for products by providing a list of suggested search queries to be passed to the search engine based on the context provided.",
        llm=basic_llm,
        verbose=True,
    )

    search_queries_recommendation_task = Task(
        description="\n".join([
            "Hope is looking to buy {product_name} at the best prices (value for a price strategy)",
            "The campany target any of these websites to buy from: {websites_list}",
            "The company wants to reach all available proucts on the internet to be compared later in another stage.",
            "The stores must sell the product in {country_name}",
            "Generate at maximum {no_keywords} queries.",
            "The search keywords must be in {language} language.",
            "Search keywords must contains specific brands, types or technologies. Avoid general keywords.",
            "The search query must reach an ecommerce webpage for product, and not a blog or listing page."
        ]),
        expected_output="A JSON object containing a list of suggested search queries.",
        output_json=SuggestedSearchQueries,
        output_file=os.path.join(output_dir, "step_1_suggested_search_queries.json"),
        agent=search_queries_recommendation_agent
    )

    search_engine_agent = Agent(
        role="Search Engine Agent",
        goal="To search for products based on the suggested search query",
        backstory="The agent is designed to help in looking for products by searching for products based on the suggested search queries.",
        llm=basic_llm,
        verbose=True,
        tools=[search_tool]
    )

    search_engine_task = Task(
        description="\n".join([
            "The task is to search for products based on the suggested search queries.",
            "You have to collect results from multiple search queries.",
            "Ignore any susbicious links or not an ecommerce single product website link.",
            "Ignore any search results with confidence score less than ({score_th}) .",
            "The search results will be used to compare prices of products from different websites.",
        ]),
        expected_output="A JSON object containing the search results.",
        output_json=AllSearchResults,
        output_file=os.path.join(output_dir, "step_2_search_results.json"),
        agent=search_engine_agent
    )

    scraping_agent = Agent(
        role="Web scraping agent",
        goal="To extract details from any website",
        backstory="The agent is designed to help in looking for required values from any website url. These details will be used to decide which best product to buy.",
        llm=basic_llm,
        tools=[scraping_tool],
        verbose=True,
    )

    scraping_task = Task(
        description="\n".join([
            "The task is to extract product details from any ecommerce store page url.",
            "The task has to collect results from multiple pages urls.",
            "Collect the best {top_recommendations_no} products from the search results.",
        ]),
        expected_output="A JSON object containing products details",
        output_json=AllExtractedProducts,
        output_file=os.path.join(output_dir, "step_3_search_results.json"),
        agent=scraping_agent
    )

    procurement_report_author_agent = Agent(
        role="Procurement Report Author Agent",
        goal="To generate a professional HTML page for the procurement report",
        backstory="The agent is designed to assist in generating a professional HTML page for the procurement report after looking into a list of products.",
        llm=basic_llm,
        verbose=True,
    )

    procurement_report_author_task = Task(
        description="\n".join([
            "The task is to generate a professional HTML page for the procurement report.",
            "You have to use Bootstrap CSS framework for a better UI.",
            "Use the provided context about the company to make a specialized report.",
            "The report will include the search results and prices of products from different websites.",
            "The report should be structured with the following sections:",
            "1. Executive Summary: A brief overview of the procurement process and key findings.",
            "2. Introduction: An introduction to the purpose and scope of the report.",
            "3. Methodology: A description of the methods used to gather and compare prices.",
            "4. Findings: Detailed comparison of prices from different websites, including tables and charts.",
            "5. Analysis: An analysis of the findings, highlighting any significant trends or observations.",
            "6. Recommendations: Suggestions for procurement based on the analysis.",
            "7. Conclusion: A summary of the report and final thoughts.",
            "8. Appendices: Any additional information, such as raw data or supplementary materials.",
        ]),

        expected_output="A professional HTML page for the procurement report.",
        output_file=os.path.join(output_dir, "step_4_procurement_report.html"),
        agent=procurement_report_author_agent,
    )

    return {
        "agents": [
            search_queries_recommendation_agent,
            search_engine_agent,
            scraping_agent,
            procurement_report_author_agent,
        ],
        "tasks": [
            search_queries_recommendation_task,
            search_engine_task,
            scraping_task,
            procurement_report_author_task,
        ]
    }
