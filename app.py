import streamlit as st
import asyncio
import json
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# Import research agent
from research_agent import ResearchAgent, export_to_markdown, export_to_json, export_to_pdf

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DeepAgents Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Initialize session state
if 'research_history' not in st.session_state:
    st.session_state.research_history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None
if 'agent' not in st.session_state:
    st.session_state.agent = None

# Title and description
st.title("🔬 DeepAgents Research Assistant")
st.markdown("""
This application uses AI-powered agents to conduct research on any topic and generate comprehensive reports.
Enter your research query below and let the agent do the work!
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key input
    api_key = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Enter your Anthropic API key"
    )

    # Model selection
    model = st.selectbox(
        "Model",
        ["claude-sonnet-4-5-20250929", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
        index=0
    )

    # Research depth
    max_iterations = st.slider("Research Depth", 1, 10, 5, help="Number of research iterations")

    st.divider()

    # Example queries
    st.header("📝 Example Queries")
    examples = [
        "Best bureau chairs under 700 euro purchasable from Netherlands",
        "Latest developments in quantum computing",
        "Comparison of project management tools for small teams",
        "Sustainable energy solutions for residential homes"
    ]

    for example in examples:
        if st.button(example, key=f"example_{examples.index(example)}", use_container_width=True):
            st.session_state.query_input = example

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Research Query")

    # Query input
    query = st.text_area(
        "Enter your research topic:",
        value=st.session_state.get('query_input', ''),
        height=100,
        placeholder="e.g., Best ergonomic office chairs under 700 euros available in Netherlands"
    )

    # Additional instructions
    additional_instructions = st.text_area(
        "Additional Instructions (Optional):",
        height=80,
        placeholder="e.g., Focus on chairs with lumbar support, include price comparisons, check availability on bol.com and coolblue.nl"
    )

    # Research button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        research_button = st.button("🚀 Start Research", type="primary", use_container_width=True)
    with col_btn2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)

    if clear_button:
        st.session_state.current_result = None
        st.rerun()

with col2:
    st.header("📊 Status")
    status_container = st.container()

# Research execution
if research_button and query:
    if not api_key:
        st.error("⚠️ Please provide an Anthropic API key in the sidebar.")
    else:
        with status_container:
            st.info("🔄 Initializing research agent...")

        try:
            # Initialize agent if not already done
            if st.session_state.agent is None:
                st.session_state.agent = ResearchAgent(
                    api_key=api_key,
                    model=model
                )

            # Combine query with additional instructions
            full_query = query
            if additional_instructions:
                full_query += f"\n\nAdditional requirements:\n{additional_instructions}"

            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Run research
            async def run_research():
                status_text.text("🔍 Conducting research...")
                progress_bar.progress(30)

                result = await st.session_state.agent.research(
                    query=full_query,
                    max_iterations=max_iterations
                )

                progress_bar.progress(100)
                status_text.text("✅ Research completed!")

                return result

            # Execute async research
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_research())
            loop.close()

            # Store result
            st.session_state.current_result = {
                'query': query,
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'model': model
            }

            # Add to history
            st.session_state.research_history.insert(0, st.session_state.current_result)

            with status_container:
                st.success("✅ Research completed successfully!")

        except Exception as e:
            with status_container:
                st.error(f"❌ Error during research: {str(e)}")
                st.exception(e)

# Display results
if st.session_state.current_result:
    st.divider()
    st.header("📄 Research Results")

    # Metadata
    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        st.metric("Query", st.session_state.current_result['query'][:30] + "...")
    with col_meta2:
        st.metric("Model", st.session_state.current_result['model'])
    with col_meta3:
        timestamp = datetime.fromisoformat(st.session_state.current_result['timestamp'])
        st.metric("Completed", timestamp.strftime("%H:%M:%S"))

    # Results display
    st.markdown("### 📋 Report")
    st.markdown(st.session_state.current_result['result'])

    # Export options
    st.divider()
    st.header("💾 Export Options")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        # Export to Markdown
        md_content = export_to_markdown(st.session_state.current_result)
        st.download_button(
            label="📝 Download as Markdown",
            data=md_content,
            file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_exp2:
        # Export to JSON
        json_content = export_to_json(st.session_state.current_result)
        st.download_button(
            label="📊 Download as JSON",
            data=json_content,
            file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    with col_exp3:
        # Export to PDF
        try:
            pdf_bytes = export_to_pdf(st.session_state.current_result)
            st.download_button(
                label="📕 Download as PDF",
                data=pdf_bytes,
                file_name=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF export error: {str(e)}")

# Research history
if st.session_state.research_history:
    st.divider()
    st.header("📚 Research History")

    for idx, item in enumerate(st.session_state.research_history[:5]):
        with st.expander(f"{item['query'][:50]}... - {item['timestamp'][:10]}"):
            st.markdown(item['result'][:500] + "...")
            if st.button(f"Load Full Result", key=f"load_{idx}"):
                st.session_state.current_result = item
                st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Powered by DeepAgents & Claude AI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
