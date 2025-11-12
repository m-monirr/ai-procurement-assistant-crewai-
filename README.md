# AI-Powered Procurement Assistant 🤖

An intelligent multi-agent system built with CrewAI that automates product research and procurement analysis for businesses. The system searches for products across multiple e-commerce platforms, extracts detailed information, and generates comprehensive procurement reports.

## 🌟 Features

- **Multi-Agent Architecture**: 4 specialized AI agents working together
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

### Workflow
```
Search Queries → Product Search → Data Extraction → Report Generation
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
```

3. **Configure API Keys**
   
   Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your actual API keys:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here
   AGENTOPS_API_KEY=your_actual_agentops_key
   TAVILY_API_KEY=tvly-dev-your_actual_tavily_key
   SCRAPEGRAPH_API_KEY=sgai-your_actual_scrapegraph_key
   ```

### Usage

Run the procurement analysis:
```bash
python main.py
```

The system will:
1. Generate search queries for coffee machines
2. Search across Egyptian e-commerce sites
3. Extract detailed product information
4. Create a comprehensive procurement report

## 📁 Project Structure

```
crewai/
├── main.py                 # Main application entry point
├── agents.py              # Agent and task definitions
├── crew.py                # Crew configuration
├── tools.py               # Custom tools (legacy)
├── schemas.py             # Pydantic data models
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── ai-agent-output/      # Generated reports and data
    ├── step_1_suggested_search_queries.json
    ├── step_2_search_results.json
    ├── step_3_search_results.json
    └── step_4_procurement_report.html
```

## 🔧 Configuration

### Supported E-commerce Sites
- Amazon Egypt (`www.amazon.eg`)
- Jumia Egypt (`www.jumia.com.eg`)
- Noon Egypt (`www.noon.com/egypt-en`)

### Customizable Parameters
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
4. **HTML Report**: Professional procurement report with:
   - Executive Summary
   - Methodology
   - Product Comparison Tables
   - Price Analysis
   - Recommendations

## 🔍 Sample Output

```json
{
  "products": [
    {
      "product_title": "De'Longhi Automatic Coffee Machine",
      "product_current_price": 5999.00,
      "product_original_price": 7999.00,
      "product_discount_percentage": 25.0,
      "agent_recommendation_rank": 5,
      "product_specs": [
        {"specification_name": "Pressure", "specification_value": "15 bar"},
        {"specification_name": "Capacity", "specification_value": "1.8L"}
      ]
    }
  ]
}
```

## 🚧 Troubleshooting

### Common Issues

1. **Unicode Encoding Error (Windows)**
   - Run in PowerShell instead of Command Prompt
   - Or use: `chcp 65001` before running

2. **LiteLLM Import Error**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

3. **API Rate Limits**
   - OpenRouter free tier has rate limits
   - Tavily free tier: 1,000 searches/month

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

