"""Web search tool for gathering information about AI trends and topics."""

import json
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from crewai.tools import tool


@tool("web_search")
def web_search(query: str, max_results: int = 10) -> str:
    """
    Search the web for current AI trends, software development topics,
    and IT industry news. Returns relevant articles, blog posts, and discussions.
    Use this tool to gather up-to-date information before writing content.

    Args:
        query: The search query string
        max_results: Maximum number of search results to return (default: 10)

    Returns:
        JSON string containing search results with title, snippet, and URL
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                keywords=query,
                max_results=max_results,
                region='wt-wt',
                safesearch='moderate'
            ))

        if not results:
            return json.dumps({
                "status": "no_results",
                "query": query,
                "results": []
            })

        # Format results for better consumption
        formatted_results = []
        for idx, result in enumerate(results, 1):
            formatted_results.append({
                "rank": idx,
                "title": result.get("title", ""),
                "snippet": result.get("body", ""),
                "url": result.get("href", ""),
            })

        return json.dumps({
            "status": "success",
            "query": query,
            "total_results": len(formatted_results),
            "results": formatted_results
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": query,
            "error": str(e),
            "results": []
        })


@tool("multi_query_search")
def multi_query_search(topic: str, queries_per_topic: int = 5, results_per_query: int = 5) -> str:
    """
    Perform multiple searches with different query formulations to get
    comprehensive coverage of a topic. Automatically generates diverse
    search queries and aggregates results.

    Args:
        topic: The main topic to research
        queries_per_topic: Number of diverse queries to generate (default: 5)
        results_per_query: Results to fetch per query (default: 5)

    Returns:
        JSON string containing aggregated search results from multiple queries
    """
    def generate_diverse_queries(topic: str, count: int) -> List[str]:
        """Generate diverse search queries for a topic."""
        queries = [
            f"{topic} latest trends 2026",
            f"{topic} breakthrough innovations",
            f"{topic} industry impact",
            f"{topic} best practices",
            f"{topic} future predictions",
            f"what's new in {topic}",
            f"{topic} case studies",
            f"{topic} expert insights"
        ]
        return queries[:count]

    try:
        queries = generate_diverse_queries(topic, queries_per_topic)
        all_results = []
        seen_urls = set()

        for query in queries:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    keywords=query,
                    max_results=results_per_query,
                    region='wt-wt',
                    safesearch='moderate'
                ))

            # Deduplicate by URL
            for result in results:
                url = result.get("href", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append({
                        "query": query,
                        "title": result.get("title", ""),
                        "snippet": result.get("body", ""),
                        "url": url
                    })

        return json.dumps({
            "status": "success",
            "topic": topic,
            "queries_used": queries,
            "total_unique_results": len(all_results),
            "results": all_results
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "topic": topic,
            "error": str(e),
            "results": []
        })
