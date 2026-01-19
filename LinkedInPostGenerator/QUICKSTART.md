# 🚀 Quick Start Guide

Get up and running with the LinkedIn AI Post Generator in 3 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your Anthropic API key:
   - Visit: https://console.anthropic.com/
   - Create account or sign in
   - Go to API Keys section
   - Create a new key

3. Open `.env` and add your key:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   ```

## Step 3: Generate Your First Post (1 minute)

```bash
python main.py generate --topic "Latest AI trends 2026"
```

That's it! 🎉

## What Happens Next?

The system will autonomously:

1. 🔍 **Research** - Search the web 5+ times with different queries
2. 📊 **Analyze** - Synthesize findings and identify key insights
3. ✍️ **Write** - Create an initial LinkedIn post draft
4. 🔍 **Critique** - Evaluate quality against 10+ criteria
5. ✨ **Refine** - Improve the post iteratively (up to 3 iterations)
6. 💾 **Save** - Store the final post in `outputs/` folder

## Example Commands

```bash
# Interactive mode (prompts for topic)
python main.py generate

# Specific topic
python main.py generate --topic "AI agents and autonomous systems"

# More refinement iterations
python main.py generate --topic "Cloud native development" --iterations 5

# View example topics
python main.py examples

# Check system info
python main.py info
```

## Troubleshooting

**Can't find .env file?**
- Make sure you copied .env.example to .env
- Use: `cp .env.example .env` (Mac/Linux) or `copy .env.example .env` (Windows)

**Import errors?**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.8+)

**API key not working?**
- Double-check you copied the full key correctly
- Make sure there are no extra spaces
- Verify the key is valid at https://console.anthropic.com/

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try different topics from `python main.py examples`
- Customize configuration in `.env` file
- Check generated posts in `outputs/` folder

## Support

Run the built-in help:
```bash
python main.py --help
python main.py setup
```

Happy posting! 🎉
