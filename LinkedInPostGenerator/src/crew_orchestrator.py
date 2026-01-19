"""Main crew orchestrator for the LinkedIn Post Generator."""

from crewai import Crew, Process, Task
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
        initial_draft = self._run_writing_phase(topic, analysis_result)

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

        research_task = Task(
            description=(
                f"Research the topic: '{topic}'\n\n"
                "Your mission:\n"
                "1. Perform multiple web searches using diverse query formulations\n"
                "2. Search for: latest trends, breakthroughs, industry impact, expert opinions, "
                "case studies, and future predictions\n"
                "3. Gather information from at least 5 different search queries\n"
                "4. Focus on recent developments (2025-2026)\n"
                "5. Look for both technical details and business implications\n"
                "6. Collect diverse perspectives from different sources\n\n"
                "Deliver a comprehensive research report that includes:\n"
                "- Key findings and trends\n"
                "- Notable developments and breakthroughs\n"
                "- Industry impact and implications\n"
                "- Expert insights and perspectives\n"
                "- Relevant statistics and data points\n"
                "- Source citations"
            ),
            expected_output=(
                "A detailed research report containing key findings about the topic, "
                "organized by themes with source citations. Include specific examples, "
                "data points, and quotes from credible sources."
            ),
            agent=research_agent
        )

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

        analyst_agent = create_analyst_agent()

        analysis_task = Task(
            description=(
                f"Analyze the following research findings about '{topic}' and synthesize insights for a LinkedIn post.\n\n"
                f"Research Findings:\n{research_result}\n\n"
                "Your analysis should:\n"
                "1. Identify the 2-3 most compelling trends or insights\n"
                "2. Find the narrative thread that connects these insights\n"
                "3. Determine what will resonate most with LinkedIn's tech professional audience\n"
                "4. Highlight actionable takeaways or thought-provoking angles\n"
                "5. Note any surprising or counterintuitive findings\n"
                "6. Consider both technical depth and business relevance\n\n"
                "Deliver:\n"
                "- Core narrative/angle for the post\n"
                "- 2-3 key insights to feature\n"
                "- Supporting data points and examples\n"
                "- Suggested tone and approach\n"
                "- Potential hooks and calls-to-action"
            ),
            expected_output=(
                "A structured analysis that identifies the core narrative, key insights, "
                "supporting evidence, and recommended approach for crafting an engaging "
                "LinkedIn post. Include specific recommendations on angle, tone, and structure."
            ),
            agent=analyst_agent
        )

        crew = Crew(
            agents=[analyst_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=self.settings.verbose
        )

        result = crew.kickoff()
        print_success("Analysis phase completed")

        return str(result)

    def _run_writing_phase(self, topic: str, analysis_result: str) -> str:
        """Run the writing phase with the writer agent."""
        print_agent_action("Writer Agent", "Crafting LinkedIn post draft...")

        writer_agent = create_writer_agent()

        writing_task = Task(
            description=(
                f"Write an engaging LinkedIn post about '{topic}' based on this analysis.\n\n"
                f"Analysis:\n{analysis_result}\n\n"
                "LinkedIn Post Requirements:\n"
                "1. Hook: Start with a compelling first line that grabs attention\n"
                "2. Structure: Use short paragraphs (2-3 lines each) for readability\n"
                "3. Content: Balance insight with accessibility - technical but not jargon-heavy\n"
                "4. Length: Aim for 150-250 words (LinkedIn's sweet spot)\n"
                "5. Formatting: Use line breaks and emojis sparingly for visual appeal\n"
                "6. Engagement: End with a question or call-to-action\n"
                "7. Hashtags: Include 3-5 relevant hashtags at the end\n\n"
                "Writing Guidelines:\n"
                "- Be authentic and conversational, not corporate\n"
                "- Use specific examples and data points\n"
                "- Make it valuable - teach something or provoke thought\n"
                "- Show personality while staying professional\n"
                "- Focus on 'why this matters' not just 'what happened'\n\n"
                "Deliver a complete, ready-to-post LinkedIn post."
            ),
            expected_output=(
                "A polished LinkedIn post (150-250 words) with:\n"
                "- Attention-grabbing opening\n"
                "- Clear, valuable insights\n"
                "- Proper formatting for LinkedIn\n"
                "- Engaging call-to-action\n"
                "- Relevant hashtags"
            ),
            agent=writer_agent
        )

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
        critic_agent = create_critic_agent()

        critique_task = Task(
            description=(
                f"Critically evaluate this LinkedIn post draft against quality standards.\n\n"
                f"Post Draft:\n{draft}\n\n"
                "Evaluation Criteria:\n"
                "1. Hook Effectiveness: Does it grab attention immediately?\n"
                "2. Value Delivery: Does it teach something or provide real insight?\n"
                "3. Clarity: Is it easy to understand? Any jargon that needs explaining?\n"
                "4. Accuracy: Are facts and claims properly supported?\n"
                "5. Structure: Is it well-organized and scannable?\n"
                "6. Engagement: Does it invite interaction or further thought?\n"
                "7. LinkedIn Optimization: Does it follow platform best practices?\n"
                "8. Authenticity: Does it feel genuine and not overly promotional?\n"
                "9. Length: Is it the right length (not too long or short)?\n"
                "10. Hashtags: Are they relevant and properly chosen?\n\n"
                "Provide:\n"
                "- Overall assessment (scale 1-10 with justification)\n"
                "- Specific strengths to preserve\n"
                "- Specific weaknesses to address\n"
                "- Concrete suggestions for improvement\n"
                "- Priority ranking of suggested changes"
            ),
            expected_output=(
                "A detailed critique with:\n"
                "- Overall quality score (1-10) and reasoning\n"
                "- What works well (to preserve in revision)\n"
                "- What needs improvement (specific issues)\n"
                "- Actionable recommendations (prioritized)\n"
                "- Whether the post is ready or needs revision"
            ),
            agent=critic_agent
        )

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
        editor_agent = create_editor_agent()

        editing_task = Task(
            description=(
                f"Refine the LinkedIn post based on the critique (Iteration {iteration}).\n\n"
                f"Original Draft:\n{draft}\n\n"
                f"Critique:\n{critique}\n\n"
                "Your refinement process:\n"
                "1. Review the original draft and critique carefully\n"
                "2. Preserve what's working well (as noted in critique)\n"
                "3. Address all high-priority issues first\n"
                "4. Make targeted improvements to weak areas\n"
                "5. Enhance clarity, flow, and impact\n"
                "6. Ensure all changes maintain the core message and insights\n"
                "7. Polish language and formatting\n\n"
                "Refinement Guidelines:\n"
                "- Make meaningful improvements, not just surface changes\n"
                "- Stay true to the original insights and narrative\n"
                "- Don't over-edit - preserve authentic voice\n"
                "- Ensure every change serves a clear purpose\n"
                "- Maintain LinkedIn best practices\n\n"
                "Deliver the refined version with a brief summary of key changes made."
            ),
            expected_output=(
                "A refined LinkedIn post that addresses the critique while preserving "
                "strengths. Include:\n"
                "- The improved post (complete and ready to publish)\n"
                "- Summary of key changes made\n"
                "- Explanation of how critique was addressed"
            ),
            agent=editor_agent
        )

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
