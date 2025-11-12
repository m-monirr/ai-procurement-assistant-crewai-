import os
from dotenv import load_dotenv
from crewai import LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from tavily import TavilyClient
from scrapegraph_py import Client

from agents import create_agents_and_tasks
from crew import create_crew

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # --- API KEYS ---
    # Get API keys from environment variables
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY") 
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SCRAPEGRAPH_API_KEY = os.getenv("SCRAPEGRAPH_API_KEY")
    
    # Validate that all required API keys are present
    required_keys = {
        "OPENROUTER_API_KEY": OPENROUTER_API_KEY,
        "AGENTOPS_API_KEY": AGENTOPS_API_KEY,
        "TAVILY_API_KEY": TAVILY_API_KEY,
        "SCRAPEGRAPH_API_KEY": SCRAPEGRAPH_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        print("Please check your .env file and make sure all API keys are set.")
        return
    
    # Set OpenAI API key for knowledge storage (use OpenRouter key)
    os.environ["OPENAI_API_KEY"] = OPENROUTER_API_KEY
    # ---

    try:
        # Initialize AgentOps
        agentops.init(api_key=AGENTOPS_API_KEY, skip_auto_end_session=True, default_tags=['crewai'])
    except Exception as e:
        print(f"AgentOps initialization warning (non-critical): {str(e)}")

    # Create output directory
    output_dir = "./ai-agent-output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize models and clients - Updated for OpenRouter with LiteLLM
    basic_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        temperature=0,
        api_key=OPENROUTER_API_KEY
    )
    search_client = TavilyClient(api_key=TAVILY_API_KEY)
    scrape_client = Client(api_key=SCRAPEGRAPH_API_KEY)

    # Company context - Simplified approach
    about_company = "Hope is a company that provides AI solutions to help websites refine their search and recommendation systems."
    
    # Create agents and tasks
    agents_and_tasks = create_agents_and_tasks(basic_llm, output_dir, search_client, scrape_client)

    # Create the crew
    hope_crew = create_crew(
        agents=agents_and_tasks["agents"],
        tasks=agents_and_tasks["tasks"],
        company_context=about_company
    )

    # Define inputs for the crew
    inputs = {
        "product_name": "coffee machine for the office",
        "websites_list": ["www.amazon.eg", "www.jumia.com.eg", "www.noon.com/egypt-en"],
        "country_name": "Egypt",
        "no_keywords": 10,
        "language": "English",
        "score_th": 0.10,
        "top_recommendations_no": 10
    }

    # Run the crew
    print("Kicking off the crew...")
    try:
        crew_results = hope_crew.kickoff(inputs=inputs)
        print("Crew run finished.")
        print("Results:", crew_results)
        
        # End AgentOps session
        agentops.end_session("Success")
    except Exception as e:
        print(f"Error during crew execution: {str(e)}")
        try:
            agentops.end_session("Error")
        except:
            pass

if __name__ == "__main__":
    main()
