from dotenv import load_dotenv
import os
import json
import asyncio
from azure.identity import AzureCliCredential,DefaultAzureCredential
from pydantic import Field
from agent_framework.azure import AzureOpenAIChatClient
from typing import Annotated
from azure.core.credentials import AzureKeyCredential
from openai import AsyncAzureOpenAI

from search_index_manager import SearchIndexManager

load_dotenv() # Load environment variables from .env file
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_AI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_AI_CHAT_DEPLOYMENT_NAME")

SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
AZURE_SEARCH_MODEL = os.getenv("AZURE_SEARCH_MODEL")

# Define embedding dimensions
embed_dimensions = 1536

# Initialize everything at module level (like your working version)
azure_search_credential = AzureKeyCredential(SEARCH_API_KEY)

# Create embeddings client that we can reference later
embeddings_client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01"
)

search_index_manager = SearchIndexManager(
    endpoint=SEARCH_ENDPOINT,
    credentials=azure_search_credential,
    model=AZURE_SEARCH_MODEL,
    api_key=SEARCH_API_KEY,
    index_name=SEARCH_INDEX_NAME,
    dimension=embed_dimensions,  # Use the defined variable
    embeddings_client=embeddings_client  # Use the defined variable
)

# define a function (tool) to fetch information from RAG
async def get_info(
    query: Annotated[str, Field(description="Get financial information from the RAG system.")],
) -> str:
    """Get financial information from the RAG system."""
    context = await search_index_manager.search(query)

    if context:
        print("📚 Retrieved context from RAG:")
        return context
    else:
        return "No specific information found in the financial knowledge base."

# define a function to get financial advice
def get_financial_advice(
    topic: Annotated[str, Field(description="The financial topic to provide advice on")]
) -> str:
    """Provide general financial advice on various topics."""
    topic = topic.lower()
    
    if 'budget' in topic:
        return "For budgeting: 1) Track all income and expenses, 2) Use the 50/30/20 rule (50% needs, 30% wants, 20% savings), 3) Review monthly and adjust as needed."
    elif 'saving' in topic or 'save' in topic:
        return "Saving strategies: 1) Start with an emergency fund (3-6 months expenses), 2) Automate savings transfers, 3) Use high-yield savings accounts, 4) Set specific savings goals."
    elif 'debt' in topic:
        return "Debt management: 1) List all debts with balances and rates, 2) Consider debt avalanche (highest interest first) or snowball (smallest balance first), 3) Avoid new debt while paying off existing ones."
    elif 'investment' in topic:
        return "Investment basics: 1) Start with emergency fund first, 2) Consider low-cost index funds, 3) Diversify your portfolio, 4) Think long-term. Always consult a financial advisor for personalized advice."
    else:
        return f"For {topic}, consider consulting financial resources or speaking with a financial advisor for personalized guidance."

# initialise a chat agent with azure openai response and a toolset (like your working version)
agent = AzureOpenAIChatClient(
         endpoint=AZURE_OPENAI_ENDPOINT,
         api_key=AZURE_OPENAI_KEY,
         deployment_name=AZURE_OPENAI_DEPLOYMENT
).create_agent(
        model=AZURE_OPENAI_DEPLOYMENT,
        name="Finance-RAG-Agent",
        instructions="""You are a helpful financial advisor assistant that provides practical, actionable advice on:
        - Budgeting and expense management
        - Saving strategies and emergency funds
        - Basic investment principles
        - Debt management
        - Financial goal setting
        
        Use the available tools to search for specific information or provide general financial advice.
        Keep your responses helpful, concise, and focused on practical financial advice. 
        Always remind users to consult with licensed financial advisors for personalized investment advice.
        Format your responses in a clear, easy-to-read way with bullet points when appropriate.""",
        tools=[get_info, get_financial_advice] 
)

async def main():
    """Main function for standalone usage"""
    try:
        await search_index_manager.ensure_index_created(
            vector_index_dimensions=embed_dimensions if embed_dimensions else 100)
        print(f"Created agent with ID: {agent.id}")
        
        # Test the agent with tool usage
        print("\n🤖 Finance RAG Agent Ready!")
        print("Ask me about financial topics like budgeting, saving, investing, or expense management.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")

        # Continuous conversation loop
        while True:
            try:
                user_query = input("You: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'bye', '']:
                    print("\n👋 Goodbye! Thanks for using the Finance RAG Agent!")
                    break
                
                print("\n🔄 Processing your request...")
                result = await agent.run(user_query)
                print(f"\n🤖 Agent: {result}\n")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error processing request: {str(e)}")
                print("Please try again or type 'quit' to exit.\n")
                
    finally:
        await search_index_manager.close()
        await embeddings_client.close()

if __name__ == "__main__":
    asyncio.run(main())