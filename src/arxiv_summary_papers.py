"""
ArXiv Research Summary Workflow

This script creates an intelligent workflow to:
1. Search arXiv for papers based on keywords
2. Retrieve and summarize the most relevant papers
"""

from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from autogen.mcp import create_toolkit
import os
import copy
import asyncio
import nest_asyncio

nest_asyncio.apply()
from typing import List

# Autogen imports
from autogen.agentchat import AssistantAgent, UserProxyAgent, a_initiate_chat

# Configuration for LLM
default_llm_config = {
    "cache_seed": 42,
    "temperature": 0.7,
    "top_p": 0.9,
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "api_type": "openai",
        }
    ],
    "timeout": 1200,
}

# Path to the arxiv MCP server
mcp_server_path = Path("mcp_arxiv.py")

# Summary Response Model
from pydantic import BaseModel, Field


class PaperSummary(BaseModel):
    title: str = Field(..., description="Original paper title")
    key_insights: List[str] = Field(..., description="3-5 key insights from the paper")
    potential_applications: List[str] = Field(
        ..., description="Potential real-world applications"
    )
    complexity_rating: int = Field(
        ...,
        description="Complexity rating from 1-5, where 1 is very accessible and 5 is highly technical",
        ge=1,
        le=5,
    )

    def format(self) -> str:
        return "\n".join(
            [
                f"**Title:** {self.title}",
                "",
                "**Key Insights:**",
                *[f"- {insight}" for insight in self.key_insights],
                "",
                "**Potential Applications:**",
                *[f"- {app}" for app in self.potential_applications],
                "",
                f"**Complexity Rating:** {self.complexity_rating}/5",
            ]
        )


# Customize LLM config for summary generation
summary_config_list = copy.deepcopy(default_llm_config)
summary_config_list["config_list"][0]["response_format"] = PaperSummary


def create_arxiv_summary_agents(keywords: str):
    """Create agents for the ArXiv summary workflow."""
    # User Proxy Agent to trigger actions
    user_proxy = UserProxyAgent(
        name="user_proxy",
        system_message="A proxy user who can execute actions and initiate workflows.",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
    )

    # ArXiv Search Agent
    arxiv_search_agent = AssistantAgent(
        name="arxiv_search_agent",
        system_message=f"""
        You are an expert research navigator specializing in finding the most relevant 
        academic papers for the given keywords: '{keywords}'.
        
        Your tasks:
        1. Search arXiv for the most relevant papers
        2. Select top 3-5 papers based on relevance and recency
        3. Retrieve full paper details
        4. Prepare papers for detailed summarization
        """,
        llm_config=default_llm_config,
    )

    # Summary Generation Agent
    summary_agent = AssistantAgent(
        name="summary_agent",
        system_message=f"""
        You are an expert academic paper summarizer. Your goal is to extract 
        and communicate the most valuable insights from research papers about '{keywords}'.
        
        For each paper, you will:
        1. Thoroughly analyze the paper's abstract and key sections
        2. Identify the most significant insights
        3. Determine potential real-world applications
        4. Assess the technical complexity
        5. Generate a structured, accessible summary
        """,
        llm_config=summary_config_list,
    )

    return user_proxy, arxiv_search_agent, summary_agent


async def create_toolkit_and_run(session: ClientSession, keywords: str) -> None:
    """
    Create toolkit and run the ArXiv summary workflow.

    Args:
        session (ClientSession): MCP client session
        keywords (str): Search keywords for arXiv
    """
    # Create a toolkit with available MCP tools
    toolkit = await create_toolkit(session=session)

    # Create agents
    user_proxy, arxiv_search_agent, summary_agent = create_arxiv_summary_agents(
        keywords
    )

    # Register MCP tools
    toolkit.register_for_llm(arxiv_search_agent)
    toolkit.register_for_execution(arxiv_search_agent)

    # Initiate interaction
    await a_initiate_chat(
        arxiv_search_agent,
        user_proxy,
        message=f"Search and summarize research papers about: {keywords}",
    )


def main(keywords: str):
    """
    Main function to run the ArXiv summary workflow.

    Args:
        keywords (str): Search keywords for arXiv
    """
    # Server parameters for MCP
    server_params = StdioServerParameters(
        command="python",
        args=[str(mcp_server_path), "stdio", "--storage-path", "arxiv_papers"],
    )

    # Run async workflow
    async def run_workflow():
        async with stdio_client(server_params) as (read, write), ClientSession(
            read, write
        ) as session:
            await session.initialize()
            await create_toolkit_and_run(session, keywords)

    # Run the async workflow
    asyncio.run(run_workflow())


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        keywords = " ".join(sys.argv[1:])
        main(keywords)
    else:
        print("Please provide search keywords")
        print("Example: python script.py machine learning transformers")
