"""Agent definitions for the LinkedIn Post Generator system."""

from crewai import Agent
from langchain_anthropic import ChatAnthropic
from typing import List
from ..tools.web_search import WebSearchTool, MultiQuerySearchTool
from ..config import get_settings


def create_llm():
    """Create and configure the Claude LLM instance."""
    settings = get_settings()
    return ChatAnthropic(
        model=settings.model_name,
        anthropic_api_key=settings.anthropic_api_key,
        temperature=0.7,
        max_tokens=4096
    )


def create_research_agent() -> Agent:
    """
    Create the Research Agent responsible for gathering information.

    This agent performs multiple web searches with diverse queries to gather
    comprehensive, up-to-date information about AI trends and tech topics.
    """
    return Agent(
        role="AI Trends Research Specialist",
        goal=(
            "Gather comprehensive, up-to-date information about current AI trends, "
            "software development innovations, and IT industry developments through "
            "multiple diverse web searches"
        ),
        backstory=(
            "You are an expert researcher specializing in artificial intelligence, "
            "software development, and technology trends. You have a talent for "
            "finding the most relevant and current information by formulating diverse "
            "search queries and synthesizing results from multiple sources. You always "
            "search from multiple angles to ensure comprehensive coverage."
        ),
        tools=[WebSearchTool(), MultiQuerySearchTool()],
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=15
    )


def create_analyst_agent() -> Agent:
    """
    Create the Analyst Agent responsible for synthesizing research.

    This agent analyzes the research results, identifies key themes, trends,
    and insights, and structures them for content creation.
    """
    return Agent(
        role="AI Insights Analyst",
        goal=(
            "Analyze research findings to identify the most compelling trends, "
            "insights, and narratives that will resonate with a LinkedIn audience "
            "of tech professionals"
        ),
        backstory=(
            "You are a senior technology analyst with deep expertise in AI and software "
            "development. You excel at identifying patterns, emerging trends, and "
            "meaningful insights from large amounts of information. You understand what "
            "content resonates with tech professionals on LinkedIn and can distill "
            "complex technical topics into engaging narratives."
        ),
        tools=[],
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_writer_agent() -> Agent:
    """
    Create the Writer Agent responsible for drafting LinkedIn posts.

    This agent crafts engaging, professional LinkedIn posts based on
    the analyzed insights and trends.
    """
    return Agent(
        role="LinkedIn Content Creator",
        goal=(
            "Create compelling, professional LinkedIn posts about AI and technology "
            "that educate, engage, and inspire tech professionals"
        ),
        backstory=(
            "You are an experienced content creator specializing in technology and AI "
            "content for LinkedIn. You know how to craft posts that balance technical "
            "depth with accessibility, use storytelling to make complex topics engaging, "
            "and structure content for maximum impact on LinkedIn. You understand the "
            "platform's best practices: hook readers in the first line, use short "
            "paragraphs, include relevant hashtags, and end with a call to action or "
            "thought-provoking question."
        ),
        tools=[],
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_critic_agent() -> Agent:
    """
    Create the Critic Agent responsible for evaluating content quality.

    This agent provides detailed, constructive critique of the drafted content,
    evaluating it against LinkedIn best practices and audience engagement criteria.
    """
    return Agent(
        role="Content Quality Critic",
        goal=(
            "Provide thorough, constructive critique of LinkedIn posts to ensure they "
            "meet the highest standards of quality, accuracy, engagement, and "
            "professionalism"
        ),
        backstory=(
            "You are a meticulous content strategist and editor with years of experience "
            "in social media marketing and technical communication. You have a critical "
            "eye for detail and evaluate content across multiple dimensions: factual "
            "accuracy, narrative flow, engagement potential, technical depth, "
            "accessibility, LinkedIn best practices, and overall impact. You provide "
            "specific, actionable feedback that helps improve content quality."
        ),
        tools=[],
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_editor_agent() -> Agent:
    """
    Create the Editor Agent responsible for refining content.

    This agent takes the original draft and critic feedback to produce
    a polished, refined final version.
    """
    return Agent(
        role="Content Editor & Refiner",
        goal=(
            "Refine and polish LinkedIn posts based on critical feedback to create "
            "the highest quality final content that maximizes engagement and impact"
        ),
        backstory=(
            "You are a skilled editor with expertise in transforming good content into "
            "great content. You excel at incorporating feedback, refining messaging, "
            "improving flow, and polishing language while preserving the core insights "
            "and narrative. You know when to be bold with changes and when to preserve "
            "what's working. Your edits always elevate the content."
        ),
        tools=[],
        llm=create_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )
