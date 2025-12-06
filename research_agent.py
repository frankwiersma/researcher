import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Any
from langchain.tools import tool
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, StateBackend, CompositeBackend
from fpdf import FPDF


class ResearchAgent:
    """
    Research agent that uses deepagents to conduct comprehensive research
    on any given topic.
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize the research agent.

        Args:
            api_key: Anthropic API key
            model: Model to use for research
        """
        self.api_key = api_key
        self.model = model
        self.backend = self._setup_backend()
        self.agent = None

        # Set API key in environment
        os.environ["ANTHROPIC_API_KEY"] = api_key

    def _setup_backend(self) -> CompositeBackend:
        """Set up the backend for the agent."""
        backend = CompositeBackend(
            default=StateBackend,
            routes={
                "/memories/": FilesystemBackend,
                "/research/": FilesystemBackend,
            }
        )
        return backend

    def _create_tools(self) -> List:
        """Create tools for the research agent."""

        @tool
        def web_search(query: str, max_results: int = 10) -> str:
            """
            Search the web for information on a given query.
            This is a simulated search - in production, integrate with
            Google, Bing, SerpAPI, or other search providers.

            Args:
                query: Search query
                max_results: Maximum number of results to return

            Returns:
                Search results as formatted text
            """
            # Simulated search results with realistic data for the example query
            if "chair" in query.lower() or "bureau" in query.lower():
                results = """
                Search Results for: {query}

                1. **Herman Miller Aeron Chair - €649**
                   - Available at: Coolblue.nl
                   - Features: Ergonomic design, lumbar support, adjustable arms
                   - Rating: 4.7/5 (1,234 reviews)
                   - URL: https://www.coolblue.nl/herman-miller-aeron

                2. **Steelcase Series 1 - €599**
                   - Available at: Bol.com
                   - Features: Weight-activated mechanism, adjustable seat depth
                   - Rating: 4.5/5 (892 reviews)
                   - URL: https://www.bol.com/steelcase-series-1

                3. **IKEA MARKUS - €199**
                   - Available at: IKEA.nl
                   - Features: High backrest, tilt function, 10-year guarantee
                   - Rating: 4.3/5 (3,456 reviews)
                   - URL: https://www.ikea.nl/markus

                4. **Secretlab TITAN Evo 2022 - €549**
                   - Available at: Secretlab.eu
                   - Features: Magnetic memory foam head pillow, 4-way lumbar support
                   - Rating: 4.8/5 (2,103 reviews)
                   - URL: https://www.secretlab.eu/titan-evo

                5. **ErgoHuman Elite - €695**
                   - Available at: Ergonomicswarehouse.nl
                   - Features: Full mesh, multi-adjustable, headrest included
                   - Rating: 4.6/5 (567 reviews)
                   - URL: https://www.ergonomicswarehouse.nl/ergohuman

                6. **HAG Capisco 8106 - €685**
                   - Available at: Flokk.com
                   - Features: Saddle seat, promotes movement, sustainable materials
                   - Rating: 4.4/5 (423 reviews)
                   - URL: https://www.flokk.com/hag-capisco

                7. **Autonomous ErgoChair Pro - €449**
                   - Available at: Autonomous.ai
                   - Features: Breathable mesh, recline and tilt functions
                   - Rating: 4.5/5 (1,890 reviews)
                   - URL: https://www.autonomous.ai/ergochair-pro

                8. **Humanscale Freedom - €650**
                   - Available at: Officecentre.nl
                   - Features: Self-adjusting recline, no manual controls needed
                   - Rating: 4.7/5 (345 reviews)
                   - URL: https://www.officecentre.nl/humanscale-freedom
                """.format(query=query)
            else:
                results = f"""
                Search Results for: {query}

                [Simulated results - integrate with real search API for production]

                Found {max_results} results related to your query.
                This is a placeholder. Please integrate with:
                - Google Custom Search API
                - Bing Search API
                - SerpAPI
                - DuckDuckGo API
                """

            return results

        @tool
        def analyze_product(product_name: str, criteria: str = "features,price,reviews") -> str:
            """
            Analyze a specific product based on given criteria.

            Args:
                product_name: Name of the product to analyze
                criteria: Comma-separated criteria (e.g., "features,price,reviews")

            Returns:
                Detailed analysis of the product
            """
            analysis = f"""
            Product Analysis: {product_name}

            Based on criteria: {criteria}

            This tool would scrape product pages, aggregate reviews,
            and provide comprehensive analysis. Integrate with:
            - Product APIs
            - Review aggregators
            - Price comparison services
            """
            return analysis

        @tool
        def summarize_research(findings: str, focus_areas: str = "") -> str:
            """
            Summarize research findings into a coherent report.

            Args:
                findings: Raw research findings to summarize
                focus_areas: Specific areas to focus on in the summary

            Returns:
                Summarized research report
            """
            summary = f"""
            Research Summary
            ================

            Focus Areas: {focus_areas if focus_areas else "General overview"}

            Key Findings:
            {findings[:500]}...

            [This tool provides AI-powered summarization of research findings]
            """
            return summary

        @tool
        def price_comparison(products: str, currency: str = "EUR") -> str:
            """
            Compare prices across different retailers for given products.

            Args:
                products: Comma-separated list of products
                currency: Currency for price comparison

            Returns:
                Price comparison table
            """
            comparison = f"""
            Price Comparison Table ({currency})
            ===================================

            Products: {products}

            [Integrate with price comparison APIs for real-time data]
            - CamelCamelCamel for Amazon
            - PriceRunner for EU markets
            - Idealo for German/EU markets
            """
            return comparison

        @tool
        def check_availability(product: str, location: str = "Netherlands") -> str:
            """
            Check product availability in specific location.

            Args:
                product: Product name
                location: Location to check availability

            Returns:
                Availability information
            """
            availability = f"""
            Availability Check
            ==================

            Product: {product}
            Location: {location}

            [Integrate with retailer APIs to check real-time stock]
            Common Dutch retailers:
            - Bol.com
            - Coolblue.nl
            - MediaMarkt.nl
            - Amazon.nl
            """
            return availability

        return [
            web_search,
            analyze_product,
            summarize_research,
            price_comparison,
            check_availability
        ]

    async def research(self, query: str, max_iterations: int = 5) -> str:
        """
        Conduct research on the given query.

        Args:
            query: Research query
            max_iterations: Maximum number of research iterations

        Returns:
            Research findings as a formatted string
        """
        # Create agent with tools
        tools = self._create_tools()

        # Create system prompt for research
        system_prompt = """You are an expert researcher. Your job is to conduct thorough research and write a polished report.

        When conducting research:
        1. Use the available tools to gather comprehensive information
        2. Search for relevant products, services, or information
        3. Compare options based on key criteria (price, features, availability, reviews)
        4. Provide specific recommendations with justifications
        5. Include sources and links where applicable
        6. Format the output as a well-structured report with clear sections

        Always provide detailed, actionable reports that directly address the research query.
        """

        self.agent = create_deep_agent(
            model=self.model,
            backend=self.backend,
            tools=tools,
            system_prompt=system_prompt,
        )

        # Execute research using the correct API (ainvoke with messages)
        result = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": query}]
        })

        # Extract the final message content
        final_message = result["messages"][-1].content

        return final_message


# Export functions
def export_to_markdown(research_data: Dict[str, Any]) -> str:
    """
    Export research results to Markdown format.

    Args:
        research_data: Dictionary containing research results

    Returns:
        Markdown formatted string
    """
    timestamp = datetime.fromisoformat(research_data['timestamp'])

    markdown = f"""# Research Report

## Query
{research_data['query']}

## Metadata
- **Generated**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
- **Model**: {research_data['model']}

---

## Results

{research_data['result']}

---

*Generated by DeepAgents Research Assistant*
"""
    return markdown


def export_to_json(research_data: Dict[str, Any]) -> str:
    """
    Export research results to JSON format.

    Args:
        research_data: Dictionary containing research results

    Returns:
        JSON formatted string
    """
    export_data = {
        'query': research_data['query'],
        'result': research_data['result'],
        'timestamp': research_data['timestamp'],
        'model': research_data['model'],
        'exported_at': datetime.now().isoformat()
    }

    return json.dumps(export_data, indent=2)


def export_to_pdf(research_data: Dict[str, Any]) -> bytes:
    """
    Export research results to PDF format.

    Args:
        research_data: Dictionary containing research results

    Returns:
        PDF as bytes
    """
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Research Report', 0, 1, 'C')
    pdf.ln(5)

    # Query
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Query:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 10, research_data['query'])
    pdf.ln(5)

    # Metadata
    timestamp = datetime.fromisoformat(research_data['timestamp'])
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} | Model: {research_data['model']}", 0, 1)
    pdf.ln(5)

    # Results
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Results:', 0, 1)
    pdf.set_font('Arial', '', 10)

    # Handle text encoding and split into lines
    result_text = research_data['result'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, result_text)

    # Footer
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, 'Generated by DeepAgents Research Assistant', 0, 1, 'C')

    # Return PDF as bytes
    # In fpdf2, output() already returns bytes when dest='S'
    return bytes(pdf.output())
