#!/usr/bin/env python3
"""
LinkedIn Post Generator - Main CLI Entry Point

An autonomous multi-agent system that generates engaging LinkedIn posts
about AI trends and software development topics.
"""

import click
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crew_orchestrator import LinkedInPostGenerator
from src.config import get_settings
from src.utils import (
    print_header,
    print_section,
    print_success,
    print_error,
    print_info,
    console
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    LinkedIn Post Generator - Autonomous AI Agent System

    Generate engaging LinkedIn posts about AI and technology trends using
    a multi-agent system that researches, analyzes, writes, critiques, and
    refines content autonomously.
    """
    pass


@cli.command()
@click.option(
    '--topic',
    '-t',
    prompt='Enter the topic for your LinkedIn post',
    help='The topic to generate a LinkedIn post about'
)
@click.option(
    '--output-dir',
    '-o',
    default='outputs',
    help='Directory to save the generated post (default: outputs)'
)
@click.option(
    '--iterations',
    '-i',
    default=3,
    type=int,
    help='Maximum refinement iterations (default: 3)'
)
@click.option(
    '--show-thinking/--no-thinking',
    default=True,
    help='Show agent thinking process (default: show)'
)
def generate(topic: str, output_dir: str, iterations: int, show_thinking: bool):
    """
    Generate a LinkedIn post about AI and technology trends.

    The agent will autonomously:
    - Search multiple times with different queries
    - Analyze and synthesize information
    - Generate an initial draft
    - Critique its own work
    - Refine the post iteratively

    Example:
        python main.py generate --topic "Latest trends in AI agents"
    """
    try:
        print_header()

        # Display configuration
        print_section("⚙️ Configuration", "⚙️")
        print_info(f"Topic: {topic}")
        print_info(f"Max Iterations: {iterations}")
        print_info(f"Output Directory: {output_dir}")
        print_info(f"Show Thinking: {show_thinking}")

        # Validate environment
        try:
            settings = get_settings()
            print_success("Configuration loaded successfully")
        except Exception as e:
            print_error(f"Configuration error: {e}")
            print_info("Make sure you have a .env file with ANTHROPIC_API_KEY")
            print_info("Copy .env.example to .env and add your API key")
            return

        # Override settings if provided
        if iterations != 3:
            settings.max_iterations = iterations
        if output_dir != 'outputs':
            settings.output_dir = Path(output_dir)
        settings.show_thinking = show_thinking

        # Generate the post
        generator = LinkedInPostGenerator()
        result = generator.generate_post(topic)

        # Success message
        console.print("\n")
        print_success("✨ Post generation completed successfully!")
        print_info(f"📁 Saved to: {result['filename']}")

    except KeyboardInterrupt:
        print_error("\n\nGeneration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        if show_thinking:
            import traceback
            console.print_exception()
        sys.exit(1)


@cli.command()
def examples():
    """Show example topics and use cases."""
    print_header()
    print_section("📚 Example Topics", "📚")

    examples_list = [
        ("AI & Machine Learning", [
            "Latest trends in Large Language Models",
            "AI agents and autonomous systems",
            "Multimodal AI applications",
            "AI safety and alignment",
            "AI in healthcare and drug discovery"
        ]),
        ("Software Development", [
            "Modern web development frameworks 2026",
            "Cloud-native architecture patterns",
            "DevOps and platform engineering trends",
            "Low-code/no-code platforms evolution",
            "Software testing automation innovations"
        ]),
        ("Emerging Technologies", [
            "Quantum computing breakthroughs",
            "Edge computing and IoT",
            "Blockchain and Web3 developments",
            "AR/VR in enterprise applications",
            "5G and network innovations"
        ]),
        ("IT Industry & Career", [
            "Future of remote work and collaboration",
            "Tech skills in highest demand",
            "Sustainable tech and green computing",
            "Cybersecurity trends and challenges",
            "Tech leadership and management"
        ])
    ]

    for category, topics in examples_list:
        console.print(f"\n[bold cyan]{category}:[/bold cyan]")
        for topic in topics:
            console.print(f"  • {topic}")

    console.print("\n[bold green]Usage:[/bold green]")
    console.print('  python main.py generate --topic "Your chosen topic"')


@cli.command()
def setup():
    """Guide through initial setup."""
    print_header()
    print_section("🔧 Setup Guide", "🔧")

    console.print("\n[bold]Step 1: Install Dependencies[/bold]")
    console.print("  pip install -r requirements.txt\n")

    console.print("[bold]Step 2: Configure API Key[/bold]")
    console.print("  1. Copy .env.example to .env")
    console.print("  2. Get your API key from: https://console.anthropic.com/")
    console.print("  3. Add it to .env: ANTHROPIC_API_KEY=your_key_here\n")

    console.print("[bold]Step 3: Test Your Setup[/bold]")
    console.print('  python main.py generate --topic "AI trends 2026"\n')

    # Check if .env exists
    env_file = Path('.env')
    if env_file.exists():
        print_success(".env file found!")
        try:
            settings = get_settings()
            print_success("API key configured!")
            print_info("You're ready to generate posts!")
        except Exception as e:
            print_error(f"Configuration issue: {e}")
    else:
        print_info(".env file not found - please create it from .env.example")


@cli.command()
def info():
    """Display system information and agent details."""
    print_header()

    print_section("🤖 Agent System Architecture", "🤖")

    agents = [
        ("Research Agent", "🔍", "Performs multi-query web searches to gather comprehensive information"),
        ("Analyst Agent", "📊", "Synthesizes research findings and identifies key insights"),
        ("Writer Agent", "✍️", "Crafts engaging LinkedIn posts following best practices"),
        ("Critic Agent", "🔍", "Evaluates content quality and provides detailed feedback"),
        ("Editor Agent", "✨", "Refines posts based on critique to maximize impact")
    ]

    for name, emoji, description in agents:
        console.print(f"\n{emoji} [bold cyan]{name}[/bold cyan]")
        console.print(f"   {description}")

    print_section("🔄 Workflow Process", "🔄")
    workflow_steps = [
        "1. Research: Multi-query web search for current information",
        "2. Analysis: Identify trends, insights, and narrative angles",
        "3. Writing: Create initial LinkedIn post draft",
        "4. Critique: Evaluate quality against 10+ criteria",
        "5. Refinement: Iteratively improve based on feedback",
        "6. Finalization: Save polished, ready-to-publish post"
    ]

    for step in workflow_steps:
        console.print(f"  {step}")

    try:
        settings = get_settings()
        print_section("⚙️ Current Configuration", "⚙️")
        console.print(f"  Model: {settings.model_name}")
        console.print(f"  Max Iterations: {settings.max_iterations}")
        console.print(f"  Search Queries: {settings.search_queries_count}")
        console.print(f"  Output Directory: {settings.output_dir}")
    except:
        print_info("\nConfigure your .env file to see settings")


if __name__ == '__main__':
    cli()
