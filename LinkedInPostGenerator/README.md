# 🤖 LinkedIn AI Post Generator - Autonomous Multi-Agent System

An intelligent, fully autonomous multi-agent system that generates engaging LinkedIn posts about AI trends, software development, and IT industry topics. Built with CrewAI and Claude, this system demonstrates true agentic behavior by researching, analyzing, writing, critiquing, and refining content autonomously.

## ✨ Features

### True Agentic Capabilities

- **🔍 Multi-Query Research**: Performs 5+ diverse web searches to gather comprehensive information
- **📊 Intelligent Analysis**: Synthesizes findings and identifies key trends and insights
- **✍️ Expert Writing**: Crafts engaging LinkedIn posts following platform best practices
- **🔍 Self-Critique**: Evaluates its own work against 10+ quality criteria
- **✨ Iterative Refinement**: Autonomously improves content until quality threshold is met
- **💭 Transparent Thinking**: Shows complete thought process and decision-making

### System Architecture

The system uses 5 specialized AI agents working in sequence:

1. **Research Agent** - Searches the web with multiple queries to gather current information
2. **Analyst Agent** - Synthesizes research and identifies compelling narratives
3. **Writer Agent** - Creates initial LinkedIn post drafts
4. **Critic Agent** - Provides detailed, constructive feedback
5. **Editor Agent** - Refines content based on critique

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or download this repository**

```bash
cd LinkedInPostGenerator
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure your API key**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

4. **Run the setup guide**

```bash
python main.py setup
```

### Generate Your First Post

```bash
python main.py generate --topic "Latest trends in AI agents"
```

## 📖 Usage

### Basic Usage

```bash
# Interactive mode (prompts for topic)
python main.py generate

# Specify topic directly
python main.py generate --topic "Your topic here"
```

### Advanced Options

```bash
# Customize refinement iterations
python main.py generate --topic "AI trends" --iterations 5

# Specify output directory
python main.py generate --topic "AI trends" --output-dir my_posts

# Hide thinking process for cleaner output
python main.py generate --topic "AI trends" --no-thinking
```

### Other Commands

```bash
# View example topics
python main.py examples

# See system architecture and configuration
python main.py info

# View setup guide
python main.py setup

# Show help
python main.py --help
```

## 🎯 Example Topics

### AI & Machine Learning
- Latest trends in Large Language Models
- AI agents and autonomous systems
- Multimodal AI applications
- AI safety and alignment
- AI in healthcare and drug discovery

### Software Development
- Modern web development frameworks 2026
- Cloud-native architecture patterns
- DevOps and platform engineering trends
- Low-code/no-code platforms evolution
- Software testing automation innovations

### Emerging Technologies
- Quantum computing breakthroughs
- Edge computing and IoT
- Blockchain and Web3 developments
- AR/VR in enterprise applications
- 5G and network innovations

### IT Industry & Career
- Future of remote work and collaboration
- Tech skills in highest demand
- Sustainable tech and green computing
- Cybersecurity trends and challenges
- Tech leadership and management

## 🔄 How It Works

The system follows a sophisticated multi-phase workflow:

```
1. RESEARCH PHASE
   └─> Research Agent performs 5+ diverse web searches
       └─> Gathers current information from multiple sources
           └─> Compiles comprehensive research report

2. ANALYSIS PHASE
   └─> Analyst Agent synthesizes findings
       └─> Identifies key trends and insights
           └─> Determines narrative angle and structure

3. WRITING PHASE
   └─> Writer Agent crafts initial draft
       └─> Follows LinkedIn best practices
           └─> Creates engaging, professional content

4. CRITIQUE PHASE (Iterative)
   └─> Critic Agent evaluates quality (1-10 scale)
       └─> Checks: hook, value, clarity, accuracy, structure, engagement
           └─> Provides specific, actionable feedback

5. REFINEMENT PHASE (Iterative)
   └─> Editor Agent refines based on critique
       └─> Makes targeted improvements
           └─> Preserves what works while fixing weaknesses

6. FINALIZATION
   └─> Saves polished post with metadata
       └─> Ready to publish on LinkedIn
```

## 📁 Project Structure

```
LinkedInPostGenerator/
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
│
├── src/
│   ├── __init__.py
│   ├── crew_orchestrator.py    # Main workflow orchestrator
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent_definitions.py   # Agent configurations
│   │   └── task_definitions.py    # Task specifications
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── web_search.py          # Custom search tools
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Configuration management
│   │
│   └── utils/
│       ├── __init__.py
│       └── console.py             # Rich CLI output utilities
│
└── outputs/                     # Generated posts (auto-created)
    └── linkedin_post_*.txt      # Saved posts with metadata
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional (defaults shown)
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_ITERATIONS=3
SEARCH_QUERIES_COUNT=5
VERBOSE=true
SHOW_THINKING=true
```

## 🎨 Output Format

Each generated post is saved with:

1. **The LinkedIn Post** - Ready to copy and paste
2. **Metadata** - Topic, timestamp, duration, model used
3. **Formatted File** - Saved in `outputs/` directory

Example output file:
```
outputs/linkedin_post_20260118_143022.txt
```

## 🔍 Transparency & Thinking Process

The system shows its complete thinking process:

- 🔍 **Research queries** being executed
- 📊 **Analysis insights** being developed
- ✍️ **Writing decisions** being made
- 🔍 **Critique evaluations** and scores
- ✨ **Refinement changes** and reasoning

This transparency helps you understand and trust the agent's work.

## 🛠️ Development

### Running in Development Mode

```bash
# Install in editable mode
pip install -e .

# Run with verbose output
python main.py generate --topic "Test" --verbose
```

### Adding Custom Agents

Extend `src/agents/agent_definitions.py` to add new specialized agents to the workflow.

### Customizing Search Behavior

Modify `src/tools/web_search.py` to adjust search strategies or add new search sources.

## 🤝 Contributing

This project demonstrates advanced agentic AI patterns. Feel free to:

- Add new agent roles
- Improve search algorithms
- Enhance critique criteria
- Optimize the refinement loop
- Add new output formats

## 📝 License

MIT License - Feel free to use and modify for your needs.

## 🙏 Acknowledgments

Built with:
- **CrewAI** - Multi-agent orchestration framework
- **Claude (Anthropic)** - Advanced language model
- **Rich** - Beautiful terminal formatting
- **DuckDuckGo Search** - Web search API

## 🐛 Troubleshooting

### "Configuration error: ANTHROPIC_API_KEY not found"
- Make sure you've created a `.env` file (copy from `.env.example`)
- Add your API key: `ANTHROPIC_API_KEY=your_actual_key`

### "Import errors" or "Module not found"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

### Search returns no results
- Check your internet connection
- DuckDuckGo search may have rate limits - wait a moment and retry

### Agent getting stuck
- Try reducing iterations: `--iterations 2`
- Check API key validity and quota
- Review error messages in verbose output

## 📧 Support

For issues or questions:
1. Check existing examples: `python main.py examples`
2. Review system info: `python main.py info`
3. Run setup guide: `python main.py setup`

---

**Built with ❤️ using Claude and CrewAI**

*Transform your LinkedIn presence with AI-powered content generation!*
