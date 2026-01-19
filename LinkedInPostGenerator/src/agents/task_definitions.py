"""Task definitions for the LinkedIn Post Generator workflow."""

from crewai import Task
from typing import List


def create_research_task(agent, topic: str) -> Task:
    """
    Create the research task for gathering information.

    Args:
        agent: The research agent
        topic: The topic to research

    Returns:
        Task instance for research
    """
    return Task(
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
        agent=agent
    )


def create_analysis_task(agent, research_task: Task) -> Task:
    """
    Create the analysis task for synthesizing research.

    Args:
        agent: The analyst agent
        research_task: The completed research task to analyze

    Returns:
        Task instance for analysis
    """
    return Task(
        description=(
            "Analyze the research findings and synthesize insights for a LinkedIn post.\n\n"
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
        agent=agent,
        context=[research_task]
    )


def create_writing_task(agent, analysis_task: Task) -> Task:
    """
    Create the writing task for drafting the LinkedIn post.

    Args:
        agent: The writer agent
        analysis_task: The completed analysis task

    Returns:
        Task instance for writing
    """
    return Task(
        description=(
            "Write an engaging LinkedIn post based on the analysis.\n\n"
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
        agent=agent,
        context=[analysis_task]
    )


def create_critique_task(agent, writing_task: Task) -> Task:
    """
    Create the critique task for evaluating the draft.

    Args:
        agent: The critic agent
        writing_task: The completed writing task to critique

    Returns:
        Task instance for critique
    """
    return Task(
        description=(
            "Critically evaluate the LinkedIn post draft against quality standards.\n\n"
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
        agent=agent,
        context=[writing_task]
    )


def create_editing_task(agent, writing_task: Task, critique_task: Task, iteration: int = 1) -> Task:
    """
    Create the editing task for refining the post.

    Args:
        agent: The editor agent
        writing_task: The original writing task
        critique_task: The completed critique task
        iteration: The current iteration number

    Returns:
        Task instance for editing
    """
    return Task(
        description=(
            f"Refine the LinkedIn post based on the critique (Iteration {iteration}).\n\n"
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
        agent=agent,
        context=[writing_task, critique_task]
    )
