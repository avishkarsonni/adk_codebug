"""Root agent initialization for ADK Bug Finder."""

from google.adk import Agent, AgentContext, Message
from typing import AsyncIterator

class RootAgent(Agent):
    """Root agent for the bug finder system."""
    
    async def run(self, context: AgentContext) -> AsyncIterator[Message]:
        """Main entry point for the bug finder agent."""
        yield Message("Starting bug analysis...")
        # Add your bug finding logic here
        yield Message("Bug analysis complete.")

# Expose the root agent
root_agent = RootAgent() 