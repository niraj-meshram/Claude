"""Rich console utilities for beautiful CLI output."""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree
from rich import box
from datetime import datetime


console = Console()


def print_header():
    """Print application header."""
    header = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        LinkedIn AI Post Generator Agent 🤖               ║
    ║        Autonomous Multi-Agent Content Creation           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold cyan")


def print_section(title: str, emoji: str = "🔍"):
    """Print a section header."""
    console.print(f"\n{emoji} [bold blue]{title}[/bold blue]")
    console.print("─" * 60, style="dim")


def print_step(step_number: int, total_steps: int, description: str):
    """Print a step indicator."""
    console.print(
        f"\n[bold yellow]Step {step_number}/{total_steps}:[/bold yellow] {description}"
    )


def print_agent_thinking(agent_name: str, thought: str):
    """Print agent's thinking process."""
    console.print(
        Panel(
            thought,
            title=f"💭 {agent_name} is thinking...",
            border_style="yellow",
            box=box.ROUNDED
        )
    )


def print_agent_action(agent_name: str, action: str):
    """Print agent's action."""
    console.print(f"  → [cyan]{agent_name}:[/cyan] {action}")


def print_success(message: str):
    """Print success message."""
    console.print(f"✅ [green]{message}[/green]")


def print_error(message: str):
    """Print error message."""
    console.print(f"❌ [red]{message}[/red]")


def print_warning(message: str):
    """Print warning message."""
    console.print(f"⚠️  [yellow]{message}[/yellow]")


def print_info(message: str):
    """Print info message."""
    console.print(f"ℹ️  [blue]{message}[/blue]")


def print_post_draft(draft: str, title: str = "LinkedIn Post Draft"):
    """Print a LinkedIn post draft in a nice panel."""
    console.print(
        Panel(
            Markdown(draft),
            title=f"📝 {title}",
            border_style="green",
            box=box.DOUBLE
        )
    )


def print_critique(critique: str):
    """Print critique in a panel."""
    console.print(
        Panel(
            critique,
            title="🔍 Content Critique",
            border_style="magenta",
            box=box.ROUNDED
        )
    )


def print_workflow_tree(current_step: str):
    """Print workflow progress tree."""
    tree = Tree("🔄 [bold]Workflow Progress[/bold]")

    steps = [
        ("Research", "🔍"),
        ("Analysis", "📊"),
        ("Writing", "✍️"),
        ("Critique", "🔍"),
        ("Editing", "✨"),
        ("Final", "🎯")
    ]

    for step, emoji in steps:
        if step.lower() in current_step.lower():
            tree.add(f"{emoji} [bold yellow]{step}[/bold yellow] ← Current")
        elif steps.index((step, emoji)) < steps.index(next((s, e) for s, e in steps if s.lower() in current_step.lower())):
            tree.add(f"{emoji} [green]{step}[/green] ✓")
        else:
            tree.add(f"{emoji} [dim]{step}[/dim]")

    console.print(tree)


def print_iteration_summary(iteration: int, max_iterations: int):
    """Print iteration summary."""
    console.print(
        Panel(
            f"Iteration {iteration} of {max_iterations}",
            title="🔄 Refinement Cycle",
            border_style="blue"
        )
    )


def save_output(content: str, filename: str):
    """Save content to file and notify user."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Saved to: {filename}")
        return True
    except Exception as e:
        print_error(f"Failed to save: {e}")
        return False


def print_final_output(post: str, metadata: dict):
    """Print the final output with metadata."""
    console.print("\n")
    console.print("═" * 70, style="bold green")
    console.print(
        Panel(
            Markdown(post),
            title="🎉 [bold green]Final LinkedIn Post[/bold green]",
            border_style="bold green",
            box=box.DOUBLE_EDGE
        )
    )

    # Print metadata table
    table = Table(title="📊 Generation Metadata", box=box.SIMPLE)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    for key, value in metadata.items():
        table.add_row(key, str(value))

    console.print(table)
    console.print("═" * 70, style="bold green")
