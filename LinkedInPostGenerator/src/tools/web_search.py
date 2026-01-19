"""Web search tool for gathering information about AI trends and topics."""

import json
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from crewai_tools import BaseTool
from pydantic import Field


class WebSearchTool(BaseTool):
    """Tool for searching the web for current AI trends and tech topics."""

    name: str = "web_search"
    description: str = (
        "Search the web for current AI trends, software development topics, "
        "and IT industry news. Returns relevant articles, blog posts, and discussions. "
        "Use this tool to gather up-to-date information before writing content."
    )
    max_results: int = Field(default=10, description="Maximum number of search results to return")

    def _run(self, query: str) -> str:
        """
        Execute a web search for the given query.

        Args:
            query: The search query string

        Returns:
            JSON string containing search results with title, body, and href
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    keywords=query,
                    max_results=self.max_results,
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


class MultiQuerySearchTool(BaseTool):
    """Tool for performing multiple diverse searches on a topic."""

    name: str = "multi_query_search"
    description: str = (
        "Perform multiple searches with different query formulations to get "
        "comprehensive coverage of a topic. Automatically generates diverse "
        "search queries and aggregates results."
    )
    queries_per_topic: int = Field(default=5, description="Number of diverse queries to generate")
    results_per_query: int = Field(default=5, description="Results to fetch per query")

    def _generate_diverse_queries(self, topic: str) -> List[str]:
        """
        Generate diverse search queries for a topic.

        Args:
            topic: The main topic to search for

        Returns:
            List of diverse search query strings
        """
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
        return queries[:self.queries_per_topic]

    def _run(self, topic: str) -> str:
        """
        Execute multiple searches for the given topic.

        Args:
            topic: The main topic to research

        Returns:
            JSON string containing aggregated search results
        """
        try:
            queries = self._generate_diverse_queries(topic)
            all_results = []
            seen_urls = set()

            for query in queries:
                with DDGS() as ddgs:
                    results = list(ddgs.text(
                        keywords=query,
                        max_results=self.results_per_query,
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
