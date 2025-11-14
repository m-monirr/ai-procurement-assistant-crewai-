# AI-Powered Procurement Assistant 🤖

An intelligent multi-agent system built with CrewAI that automates product research and procurement analysis for businesses. The system searches for products across multiple e-commerce platforms, extracts detailed information, and generates comprehensive procurement reports.

## 🌟 Features

- **Multi-Agent Architecture**: 4 specialized AI agents working together
- **YAML Configuration**: Clean agent and task definitions using YAML
- **Smart Search**: AI-generated search queries for optimal product discovery
- **Web Scraping**: Automated extraction of product details and pricing
- **Comprehensive Reports**: Professional HTML reports with Bootstrap UI
- **Price Comparison**: Compare products across multiple e-commerce platforms
- **Egyptian Market Focus**: Optimized for Egyptian e-commerce sites

## 🏗️ Architecture

### Agents
1. **Search Queries Recommendation Agent**: Generates targeted search queries
2. **Search Engine Agent**: Searches for products using Tavily API
3. **Web Scraping Agent**: Extracts detailed product information
4. **Procurement Report Author**: Creates professional HTML reports

### Project Structure
```
research_crew/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env.example
├── .env
├── run.py
├── schemas.py
├── ai-agent-output/
└── src/
    └── research_crew/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- API Keys for:
  - OpenRouter (for Llama 3.3 70B model)
  - Tavily (for web search)
  - ScrapeGraph (for web scraping)
  - AgentOps (for monitoring)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-procurement-assistant.git
cd ai-procurement-assistant
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
# or with poetry
poetry install
```

3. **Configure API Keys**
   
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your actual API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_key_here
   AGENTOPS_API_KEY=your_agentops_key_here
   TAVILY_API_KEY=your_tavily_key_here
   SCRAPEGRAPH_API_KEY=your_scrapegraph_key_here
   ```

### Usage

Run the procurement analysis:
```bash
python run.py
```

The system will:
1. Generate search queries for coffee machines
2. Search across Egyptian e-commerce sites
3. Extract detailed product information
4. Create a comprehensive procurement report

## 🔧 Configuration

### Supported E-commerce Sites
- Amazon Egypt (`www.amazon.eg`)
- Jumia Egypt (`www.jumia.com.eg`)
- Noon Egypt (`www.noon.com/egypt-en`)

### Customizable Parameters
Edit the `inputs` dictionary in `src/research_crew/main.py`:
```python
inputs = {
    "product_name": "coffee machine for the office",
    "websites_list": ["www.amazon.eg", "www.jumia.com.eg", "www.noon.com/egypt-en"],
    "country_name": "Egypt",
    "no_keywords": 10,
    "language": "English",
    "score_th": 0.10,
    "top_recommendations_no": 10
}
```

## 🛠️ API Keys Setup

### 1. OpenRouter (FREE)
- Visit: https://openrouter.ai/
- Sign up and get API key
- Used for: Llama 3.3 70B model

### 2. Tavily (FREE TIER)
- Visit: https://tavily.com/
- Get API key (1,000 searches/month free)
- Used for: Web search functionality

### 3. ScrapeGraph (PAID)
- Visit: https://scrapegraphai.com/
- Get API key
- Used for: AI-powered web scraping

### 4. AgentOps (FREE)
- Visit: https://agentops.ai/
- Get API key
- Used for: Agent monitoring and analytics

## 📊 Output

The system generates:

1. **Search Queries JSON**: AI-generated search terms
2. **Search Results JSON**: Aggregated search results
3. **Product Data JSON**: Detailed product information
4. **HTML Report**: Professional procurement report

## 🚧 Troubleshooting

### Common Issues

1. **LLM Provider Error**
   - Make sure OpenRouter API key is valid
   - Check internet connectivity

2. **Import Errors**
   - Ensure all dependencies are installed
   - Run from the project root directory

3. **Unicode Encoding Error (Windows)**
   - Run in PowerShell instead of Command Prompt

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Hope

Hope is a company that provides AI solutions to help websites refine their search and recommendation systems. This procurement assistant demonstrates our AI capabilities in automated business processes.

---

**Built with ❤️ using CrewAI and Llama 3.3 70B**

