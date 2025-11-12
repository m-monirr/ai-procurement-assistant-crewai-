import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM
import agentops
from tavily import TavilyClient
from scrapegraph_py import Client

# Add the root directory to sys.path to import schemas
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

try:
    from schemas import SuggestedSearchQueries, AllSearchResults, AllExtractedProducts
except ImportError as e:
    print(f"Error importing schemas: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Root directory: {root_dir}")
    sys.exit(1)

from .crew import ResearchCrew

def run():
    """Run the research crew."""
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
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
    # ---

    try:
        # Initialize AgentOps
        agentops.init(api_key=AGENTOPS_API_KEY, skip_auto_end_session=True, default_tags=['crewai'])
    except Exception as e:
        print(f"AgentOps initialization warning (non-critical): {str(e)}")

    # Create output directory (use absolute path)
    output_dir = os.path.join(str(root_dir), "ai-agent-output")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize models and clients - Updated for OpenRouter with LiteLLM
    basic_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        temperature=0,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    search_client = TavilyClient(api_key=TAVILY_API_KEY)
    scrape_client = Client(api_key=SCRAPEGRAPH_API_KEY)

    # Initialize the research crew
    research_crew = ResearchCrew(search_client, scrape_client, output_dir, basic_llm)
    
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
    print("Kicking off the research crew...")
    try:
        result = research_crew.crew().kickoff(inputs=inputs)
        print("Crew run finished.")
        print("Results:", result)
        
        # End AgentOps session
        agentops.end_session("Success")
    except Exception as e:
        print(f"Error during crew execution: {str(e)}")
        try:
            agentops.end_session("Error")
        except:
            pass

if __name__ == "__main__":
    run()
