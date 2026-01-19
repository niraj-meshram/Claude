"""Main crew orchestrator for the LinkedIn Post Generator."""

from crewai import Crew, Process
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json

from .agents import (
    create_research_agent,
    create_analyst_agent,
    create_writer_agent,
    create_critic_agent,
    create_editor_agent,
    create_research_task,
    create_analysis_task,
    create_writing_task,
    create_critique_task,
    create_editing_task,
)
from .config import get_settings
from .utils import (
    print_section,
    print_step,
    print_agent_action,
    print_success,
    print_error,
    print_post_draft,
    print_critique,
    print_workflow_tree,
    print_iteration_summary,
    save_output,
    print_final_output,
    console
)


class LinkedInPostGenerator:
    """
    Orchestrates the multi-agent system for generating LinkedIn posts.

    This class manages the workflow of multiple specialized agents that work
    together to research, analyze, write, critique, and refine LinkedIn posts
    about AI and technology trends.
    """

    def __init__(self):
        """Initialize the post generator with settings."""
        self.settings = get_settings()
        self.output_dir = Path(self.settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_post(self, topic: str) -> Dict[str, Any]:
        """
        Generate a LinkedIn post on the given topic.

        Args:
            topic: The topic to generate a post about

        Returns:
            Dictionary containing the final post and metadata
        """
        start_time = datetime.now()

        print_section("🚀 Starting Autonomous Post Generation", "🚀")
        print_agent_action("System", f"Topic: {topic}")
        print_agent_action("System", f"Max Iterations: {self.settings.max_iterations}")

        # Phase 1: Research
        print_workflow_tree("research")
        print_step(1, 5, "Research Phase")
        research_result = self._run_research_phase(topic)

        # Phase 2: Analysis
        print_workflow_tree("analysis")
        print_step(2, 5, "Analysis Phase")
        analysis_result = self._run_analysis_phase(topic, research_result)

        # Phase 3: Initial Writing
        print_workflow_tree("writing")
        print_step(3, 5, "Writing Phase")
        initial_draft = self._run_writing_phase(analysis_result)

        # Phase 4 & 5: Iterative Critique and Refinement
        final_post = self._run_refinement_loop(initial_draft)

        # Finalization
        print_workflow_tree("final")
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        metadata = {
            "Topic": topic,
            "Generated At": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Duration": f"{duration:.1f} seconds",
            "Iterations": self.settings.max_iterations,
            "Model": self.settings.model_name
        }

        # Save output
        timestamp = end_time.strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"linkedin_post_{timestamp}.txt"
        self._save_post_with_metadata(final_post, metadata, filename)

        # Display final output
        print_final_output(final_post, metadata)

        return {
            "post": final_post,
            "metadata": metadata,
            "filename": str(filename)
        }

    def _run_research_phase(self, topic: str) -> str:
        """Run the research phase with the research agent."""
        print_agent_action("Research Agent", "Initiating multi-query web search...")

        research_agent = create_research_agent()
        research_task = create_research_task(research_agent, topic)

        crew = Crew(
            agents=[research_agent],
            tasks=[research_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        print_success("Research phase completed")

        return str(result)

    def _run_analysis_phase(self, topic: str, research_result: str) -> str:
        """Run the analysis phase with the analyst agent."""
        print_agent_action("Analyst Agent", "Synthesizing research findings...")

        research_agent = create_research_agent()
        analyst_agent = create_analyst_agent()

        research_task = create_research_task(research_agent, topic)
        # Manually set the output from previous phase
        research_task.output = type('TaskOutput', (), {'raw': research_result})()

        analysis_task = create_analysis_task(analyst_agent, research_task)

        crew = Crew(
            agents=[analyst_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        print_success("Analysis phase completed")

        return str(result)

    def _run_writing_phase(self, analysis_result: str) -> str:
        """Run the writing phase with the writer agent."""
        print_agent_action("Writer Agent", "Crafting LinkedIn post draft...")

        analyst_agent = create_analyst_agent()
        writer_agent = create_writer_agent()

        # Create dummy analysis task with the result
        analysis_task = create_analysis_task(analyst_agent, None)
        analysis_task.output = type('TaskOutput', (), {'raw': analysis_result})()

        writing_task = create_writing_task(writer_agent, analysis_task)

        crew = Crew(
            agents=[writer_agent],
            tasks=[writing_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        draft = str(result)

        print_success("Initial draft completed")
        print_post_draft(draft, "Initial Draft")

        return draft

    def _run_refinement_loop(self, initial_draft: str) -> str:
        """
        Run the iterative critique and refinement loop.

        Args:
            initial_draft: The initial post draft

        Returns:
            The final refined post
        """
        current_draft = initial_draft

        for iteration in range(1, self.settings.max_iterations + 1):
            print_step(4 + iteration, 5 + self.settings.max_iterations,
                      f"Refinement Iteration {iteration}")
            print_iteration_summary(iteration, self.settings.max_iterations)

            # Critique phase
            print_agent_action("Critic Agent", "Evaluating post quality...")
            critique = self._run_critique_phase(current_draft)

            print_critique(critique)

            # Check if we should stop refining
            if "ready to publish" in critique.lower() or "score: 9" in critique.lower() or "score: 10" in critique.lower():
                print_success(f"Post quality threshold met at iteration {iteration}!")
                break

            # Editing phase
            print_agent_action("Editor Agent", "Refining based on feedback...")
            current_draft = self._run_editing_phase(current_draft, critique, iteration)

            print_post_draft(current_draft, f"Draft after Iteration {iteration}")

        print_success("Refinement loop completed")
        return current_draft

    def _run_critique_phase(self, draft: str) -> str:
        """Run the critique phase with the critic agent."""
        writer_agent = create_writer_agent()
        critic_agent = create_critic_agent()

        # Create dummy writing task with the draft
        writing_task = create_writing_task(writer_agent, None)
        writing_task.output = type('TaskOutput', (), {'raw': draft})()

        critique_task = create_critique_task(critic_agent, writing_task)

        crew = Crew(
            agents=[critic_agent],
            tasks=[critique_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        return str(result)

    def _run_editing_phase(self, draft: str, critique: str, iteration: int) -> str:
        """Run the editing phase with the editor agent."""
        writer_agent = create_writer_agent()
        critic_agent = create_critic_agent()
        editor_agent = create_editor_agent()

        # Create dummy tasks with previous outputs
        writing_task = create_writing_task(writer_agent, None)
        writing_task.output = type('TaskOutput', (), {'raw': draft})()

        critique_task = create_critique_task(critic_agent, writing_task)
        critique_task.output = type('TaskOutput', (), {'raw': critique})()

        editing_task = create_editing_task(editor_agent, writing_task, critique_task, iteration)

        crew = Crew(
            agents=[editor_agent],
            tasks=[editing_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        return str(result)

    def _save_post_with_metadata(self, post: str, metadata: Dict[str, Any], filename: Path):
        """Save the post along with metadata."""
        content = f"""{'='*70}
LINKEDIN POST
{'='*70}

{post}

{'='*70}
METADATA
{'='*70}

{json.dumps(metadata, indent=2)}
"""
        save_output(content, str(filename))
