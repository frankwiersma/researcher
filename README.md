# DeepAgents Research Assistant

A powerful Streamlit-based research application that uses AI agents to conduct comprehensive research and generate detailed reports. Built with DeepAgents and Claude AI.

## Features

- **AI-Powered Research**: Uses Claude AI with DeepAgents framework for autonomous research
- **Interactive Web Interface**: Clean Streamlit UI for easy interaction
- **Multiple Export Formats**: Export results as Markdown, JSON, or PDF
- **Customizable Research Depth**: Control the thoroughness of research
- **Research History**: Keep track of previous research sessions
- **Tool Integration**: Includes web search, product analysis, price comparison, and more

## Example Use Case

The application comes pre-configured with an example research query:

**"Best bureau chairs under 700 euro purchasable from Netherlands"**

This demonstrates the system's ability to:
- Search for products within specific criteria
- Compare prices across retailers
- Analyze features and reviews
- Provide actionable recommendations
- Check availability in specific regions

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup Steps

1. **Clone or download this repository**

```bash
cd researcher
```

2. **Install dependencies**

Using uv (recommended):
```bash
uv pip install -r requirements.txt
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

4. **Run the application**

```bash
streamlit run app.py --server.port 8502
```

Or use the provided scripts:
- Windows: `run.bat`
- Linux/Mac: `bash run.sh`

The application will open in your default web browser at `http://localhost:8502`

## Usage

### Basic Research

1. **Enter your research query** in the text area
2. **Add optional instructions** for specific requirements
3. **Configure settings** in the sidebar:
   - API Key (if not in .env)
   - Model selection
   - Research depth
4. **Click "Start Research"** to begin
5. **View results** in the main panel
6. **Export** results in your preferred format

### Example Queries

The sidebar includes several pre-configured example queries:

- Best bureau chairs under 700 euro purchasable from Netherlands
- Latest developments in quantum computing
- Comparison of project management tools for small teams
- Sustainable energy solutions for residential homes

Click any example to load it into the query field.

### Export Options

Results can be exported in three formats:

- **Markdown (.md)**: Clean, readable format for documentation
- **JSON (.json)**: Structured data for further processing
- **PDF (.pdf)**: Formatted document for sharing

## Architecture

### Components

1. **app.py**: Main Streamlit interface
   - User input handling
   - Results display
   - Export functionality
   - Session management

2. **research_agent.py**: Research logic and agent configuration
   - ResearchAgent class
   - Tool definitions (web_search, analyze_product, etc.)
   - Export functions

3. **requirements.txt**: Python dependencies

### Tools Available to the Agent

The research agent has access to several tools:

- **web_search**: Search for information (configure with real API in production)
- **analyze_product**: Detailed product analysis
- **summarize_research**: AI-powered summarization
- **price_comparison**: Compare prices across retailers
- **check_availability**: Check product availability by location

## Customization

### Adding Real Search Integration

The current implementation uses simulated search results. To integrate real search:

1. Choose a search API:
   - Google Custom Search API
   - Bing Search API
   - SerpAPI
   - DuckDuckGo API

2. Update the `web_search` tool in `research_agent.py`:

```python
@tool
def web_search(query: str, max_results: int = 10) -> str:
    import requests

    # Example with SerpAPI
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),
        "num": max_results
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    # Format and return results
    return format_search_results(results)
```

### Adding New Tools

Add new tools to the `_create_tools()` method in `research_agent.py`:

```python
@tool
def your_custom_tool(param: str) -> str:
    """
    Description of your tool.

    Args:
        param: Description of parameter

    Returns:
        Tool output
    """
    # Your implementation
    return result
```

### Customizing the UI

Modify `app.py` to customize:

- Layout and styling
- Additional input fields
- Custom export formats
- Integration with other services

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `DEFAULT_MODEL`: Default Claude model to use
- `MAX_RESEARCH_ITERATIONS`: Default research depth

### Model Options

Available Claude models:

- `claude-sonnet-4-5-20250929`: Latest Sonnet model (recommended)
- `claude-3-5-sonnet-20241022`: Previous Sonnet version
- `claude-3-opus-20240229`: Most capable model for complex research

## Troubleshooting

### Common Issues

**"Please provide an Anthropic API key"**
- Ensure your API key is set in `.env` or entered in the sidebar
- Verify the key is valid at https://console.anthropic.com/

**"Module not found" errors**
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure you're using Python 3.8 or higher

**PDF export errors**
- Check that fpdf2 is installed: `pip install fpdf2`
- Some special characters may not render in PDF; they're automatically handled

**Slow research**
- Reduce the "Research Depth" slider in the sidebar
- Use a faster model (Sonnet instead of Opus)
- Check your internet connection

## Development

### Project Structure

```
researcher/
├── app.py                  # Main Streamlit application
├── research_agent.py       # Research agent and tools
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual environment variables (git-ignored)
└── README.md              # This file
```

### Adding Features

1. **New research tools**: Add to `_create_tools()` in `research_agent.py`
2. **UI enhancements**: Modify `app.py`
3. **Export formats**: Add new export functions to `research_agent.py`
4. **API integrations**: Add to respective tool implementations

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues, questions, or suggestions:

1. Check the troubleshooting section above
2. Review the DeepAgents documentation
3. Check Anthropic's Claude documentation
4. Open an issue in the repository

## Credits

Built with:

- [Streamlit](https://streamlit.io/) - Web interface
- [DeepAgents](https://github.com/anthropics/deepagents) - Agent framework
- [Claude AI](https://www.anthropic.com/claude) - Language model
- [LangChain](https://langchain.com/) - Tool integration

## Roadmap

Future enhancements:

- [ ] Real-time web search integration
- [ ] Multi-language support
- [ ] Advanced analytics and visualization
- [ ] Collaborative research features
- [ ] API endpoint for programmatic access
- [ ] Integration with more data sources
- [ ] Customizable research templates
- [ ] Research comparison and diff tools

---

**Happy Researching!** 🔬
