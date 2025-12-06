# Quick Start Guide

Get started with DeepAgents Research Assistant in 3 simple steps!

## Step 1: Install Dependencies

### Using uv (Recommended - Fast!)
```bash
uv pip install -r requirements.txt
```

### Or using pip
```bash
pip install -r requirements.txt
```

Or use the automated scripts:
- Windows: Double-click `run.bat`
- Linux/Mac: Run `bash run.sh` (make it executable first: `chmod +x run.sh`)

## Step 2: Configure API Key

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

   Get your API key from: https://console.anthropic.com/

## Step 3: Run the Application

### Option A: Using Scripts (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
bash run.sh
```

### Option B: Manual Start

```bash
streamlit run app.py --server.port 8502
```

## First Research Query

Once the app opens in your browser (http://localhost:8502):

1. **Try the Example Query**: Click on the first example in the sidebar:
   - "Best bureau chairs under 700 euro purchasable from Netherlands"

2. **Or Enter Your Own Query**: Type any research topic in the text area

3. **Click "Start Research"**: The AI agent will begin researching

4. **View Results**: The report will appear with:
   - Product recommendations
   - Price comparisons
   - Feature analysis
   - Availability information

5. **Export Results**: Download as Markdown, JSON, or PDF

## Example Queries to Try

### Product Research
```
Best noise-cancelling headphones under 300 euros available in Europe
```

### Market Analysis
```
Compare top 5 project management tools for remote teams in 2024
```

### Technology Research
```
Latest developments in renewable energy storage solutions
```

### Comparative Research
```
Python vs JavaScript for web development: comprehensive comparison
```

## Customizing Your Research

### Add Specific Requirements

Use the "Additional Instructions" field:

```
Focus on:
- Products with warranty of at least 2 years
- Must ship to Netherlands
- Include customer review summaries
- Compare shipping costs
```

### Adjust Research Depth

Use the sidebar slider:
- **1-3**: Quick overview
- **4-6**: Balanced research (recommended)
- **7-10**: Deep, comprehensive analysis

### Choose Your Model

- **claude-sonnet-4-5-20250929**: Latest, fastest, most efficient (recommended)
- **claude-3-opus-20240229**: Most thorough for complex research

## Troubleshooting

### "Please provide an Anthropic API key"
- Check that `.env` file exists
- Verify your API key is correct
- Or enter the key in the sidebar

### Application won't start
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Try running directly
streamlit run app.py
```

### Slow performance
- Reduce research depth slider
- Use faster model (Sonnet)
- Check internet connection

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize tools in `research_agent.py`
- Add real search API integration (see README)
- Modify UI in `app.py` for your needs

## Tips for Best Results

1. **Be Specific**: Include details like budget, location, requirements
2. **Use Additional Instructions**: Add context and constraints
3. **Start with Examples**: Modify the example queries to learn
4. **Export Often**: Save interesting research for future reference
5. **Review History**: Learn from previous queries

---

**Need Help?**

Check the full documentation in README.md or review the code comments in:
- `app.py` - Interface and display logic
- `research_agent.py` - Research tools and agent configuration

Happy Researching! 🔬
