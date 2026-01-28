from dotenv import load_dotenv
import logging
import os
import requests
import asyncio
from azure.identity import AzureCliCredential,DefaultAzureCredential
from pydantic import Field, BaseModel
from agent_framework.azure import AzureOpenAIChatClient
from typing import Annotated, cast, Optional
from azure.core.credentials import AzureKeyCredential
from openai import AsyncAzureOpenAI
from search_index_manager import SearchIndexManager
from stock_data_manager import StockDataManager
from agent_framework import (
    ai_function,
    AgentExecutor, 
    AgentRunUpdateEvent, 
    WorkflowBuilder, 
    WorkflowOutputEvent,
    WorkflowStatusEvent, 
    WorkflowViz, 
    AgentExecutorResponse,
    MagenticBuilder,
    ChatAgent,
    ChatMessage)
try:
    from agent_framework import MAGENTIC_EVENT_TYPE_AGENT_DELTA, MAGENTIC_EVENT_TYPE_ORCHESTRATOR
    HAS_STREAMING_CONSTANTS = True
except ImportError:
    # Define fallback values if not available
    MAGENTIC_EVENT_TYPE_AGENT_DELTA = "agent_delta"
    MAGENTIC_EVENT_TYPE_ORCHESTRATOR = "orchestrator"
    HAS_STREAMING_CONSTANTS = False
    print("⚠️ Advanced streaming features not available in this agent_framework version")
# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv() # Load environment variables from .env file
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_AI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_AI_CHAT_DEPLOYMENT_NAME")

SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
AZURE_SEARCH_MODEL = os.getenv("AZURE_SEARCH_MODEL")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Define embedding dimensions
embed_dimensions = 1536

# Initialize everything at module level 
azure_search_credential = AzureKeyCredential(SEARCH_API_KEY)

# Create embeddings client that we can reference later
embeddings_client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01"
)

# Initialize managers
search_index_manager = SearchIndexManager(
    endpoint=SEARCH_ENDPOINT,
    credentials=azure_search_credential,
    model=AZURE_SEARCH_MODEL,
    api_key=SEARCH_API_KEY,
    index_name=SEARCH_INDEX_NAME,
    dimension=embed_dimensions,  # Use the defined variable
    embeddings_client=embeddings_client  # Use the defined variable
)

stock_data_manager = StockDataManager(api_key=ALPHA_VANTAGE_API_KEY)

# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

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

def get_stock_data(
    symbol: Annotated[str, Field(description="The stock ticker symbol to retrieve data for (e.g., IBM, AAPL, TSLA)")],
    interval: Annotated[str, Field(description="Time interval: 1min, 5min, 15min, 30min, or 60min. Default is 5min")] = "5min",
    outputsize: Annotated[str, Field(description="Data size: 'compact' for latest 100 points or 'full' for 30 days. Default is compact")] = "compact"
) -> str:
    """
    Get real-time and historical stock price data from Alpha Vantage API.
    Returns intraday OHLCV (Open, High, Low, Close, Volume) time series data.
    """
    return stock_data_manager.get_stock_data(symbol, interval, outputsize)

@ai_function(approval_mode="always_require")
def ask_user(question: Annotated[str, "The question to ask the user for clarification"]) -> str:
    """Ask the user a clarifying question to gather missing information.

    Use this tool when you need additional information from the user to complete
    your task effectively.
    """
    # This function body is a placeholder - the actual interaction happens via HITL.
    return f"User was asked: {question}"

# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

#initialise a manager agent for orchestration
manager_agent = AzureOpenAIChatClient(
         endpoint=AZURE_OPENAI_ENDPOINT,
         api_key=AZURE_OPENAI_KEY,
         deployment_name=AZURE_OPENAI_DEPLOYMENT
).create_agent(
        model=AZURE_OPENAI_DEPLOYMENT,
        name="MagenticManager",
        instructions="""You coordinate a team of specialized financial agents to complete complex tasks efficiently.
    
    You have access to:
    - AdvisorAgent: For budgeting, saving, debt management advice
    - ResearchAgent: For searching financial knowledge base
    - InvestmentAgent: For stock data and investment analysis
    
    Delegate tasks to the appropriate specialist and synthesize their responses into comprehensive answers.""",
        description="Orchestrator that coordinates the research,advisor, stock and investment workflow"
)

# manager_agent = ChatAgent(
#     name="MagenticManager",
#     description="Orchestrator that coordinates the research, advisor, stock and investment workflow",
#     instructions="""You coordinate a team of specialized financial agents to complete complex tasks efficiently.
    
#     You have access to:
#     - AdvisorAgent: For budgeting, saving, debt management advice
#     - ResearchAgent: For searching financial knowledge base
#     - InvestmentAgent: For stock data and investment analysis
    
#     Delegate tasks to the appropriate specialist and synthesize their responses into comprehensive answers.""",
#     chat_client=AzureOpenAIChatClient(
#         endpoint=AZURE_OPENAI_ENDPOINT,
#         api_key=AZURE_OPENAI_KEY,
#         deployment_name=AZURE_OPENAI_DEPLOYMENT,
#         #model_id=AZURE_OPENAI_DEPLOYMENT
#     )
# )

# initialise a advisor agent for financial guidance
advisor_agent = AzureOpenAIChatClient(
         endpoint=AZURE_OPENAI_ENDPOINT,
         api_key=AZURE_OPENAI_KEY,
         deployment_name=AZURE_OPENAI_DEPLOYMENT
).create_agent(
        model=AZURE_OPENAI_DEPLOYMENT,
        name="AdvisorAgent",
        instructions="""Youre are a helpful financial advisor assistant that provides practical, actionable advice on:
        - Budgeting and expense management
        - Saving strategies and emergency funds
        - Basic investment principles
        - Debt management
        - Financial goal setting
        - Stock options
        
        
        Use the available tools to search for specific information or provide general financial advice.
        Keep your responses helpful, concise, and focused on practical financial advice. 
        Always remind users to consult with licensed financial advisors for personalized investment advice.
        Format your responses in a clear, easy-to-read way with bullet points when appropriate.""",
        description="Provides personalized financial guidance on budgeting, savings, debt management, and investment strategies",
        tools=[get_financial_advice] 
)

# initialise a research agent with azure openai response and a toolset (like your working version)
research_agent = AzureOpenAIChatClient(
         endpoint=AZURE_OPENAI_ENDPOINT,
         api_key=AZURE_OPENAI_KEY,
         deployment_name=AZURE_OPENAI_DEPLOYMENT
).create_agent(
        model=AZURE_OPENAI_DEPLOYMENT,
        name="ResearchAgent",
        description="Specialist in research and information gathering from knowledge base",
        instructions="""You are a financial research specialist that retrieves information from the knowledge base.
    
    Your role is to:
    - Search the financial knowledge base for relevant information
    - Provide accurate, cited information from trusted sources
    - Help answer specific questions about financial concepts, regulations, and best practices
    
    Use the get_info tool to search the knowledge base. Present findings clearly and cite sources when available.""",
        tools=[get_info] 
)
# initialise a stocks and investment agent for market analysis and investment guidance
investment_agent = AzureOpenAIChatClient(
         endpoint=AZURE_OPENAI_ENDPOINT,
         api_key=AZURE_OPENAI_KEY,
         deployment_name=AZURE_OPENAI_DEPLOYMENT
).create_agent(
        model=AZURE_OPENAI_DEPLOYMENT,
        name="InvestmentAgent",
        instructions="""You are a knowledgeable investment and stock market specialist that provides educational information on:
        - Stock market fundamentals and analysis
        - Portfolio diversification strategies
        - Risk assessment and management
        - Investment vehicles (stocks, bonds, ETFs, mutual funds)
        - Long-term vs short-term investment strategies
        - Market trends and economic indicators
        
        Use available tools to research specific stocks, market data, or investment concepts.
        Provide clear, educational responses that help users understand investment principles.
        ALWAYS emphasize that you provide educational information only, not personalized investment advice.
        Remind users to conduct thorough research and consult licensed financial advisors before making investment decisions.
        Present information in a structured format with clear explanations.""",
        description="Specialist in stock market analysis, investment strategies, and portfolio management guidance",
        tools=[get_stock_data,ask_user]
)

# ============================================================================
# WORKFLOW SETUP
# ============================================================================

# Build the Magentic workflow by chaining agents using edge
workflow = (
    MagenticBuilder()
    .participants(
        investment=investment_agent, 
        advisor=advisor_agent, 
        research=research_agent
        )
    .with_standard_manager(
        manager=manager_agent
        #max_round_count=10,  # Maximum collaboration rounds
        #max_stall_count=3,   # Maximum rounds without progress
        #max_reset_count=2,   # Maximum plan resets allowed
    )
    #.with_plan_review()  # Enable plan review
    .build()
)

# ============================================================================
# MAIN INTERACTIVE LOOP
# ============================================================================

async def main():
    """Main function with interactive chat loop"""
    try:
        # Initialize search index
        await search_index_manager.ensure_index_created(
            vector_index_dimensions=embed_dimensions if embed_dimensions else 100)
        
        print("\n" + "="*70)
        print("🤖 Finance AI Agent Team Ready!")
        print("="*70)
        print("\nYour AI-powered financial advisory team includes:")
        print("  📊 Investment Agent - Stock data & market analysis")
        print("  💰 Advisor Agent - Budgeting & financial planning")
        print("  📚 Research Agent - Knowledge base search")
        print("  🎯 Manager Agent - Coordinates the team")
        print("\nAsk me about:")
        print("  • Stock prices and market data (e.g., 'What's the price of AAPL?')")
        print("  • Budgeting and saving strategies")
        print("  • Investment advice and portfolio management")
        print("  • Debt management and financial planning")
        print("\nType 'quit', 'exit', or 'bye' to end the conversation.\n")
        print("="*70 + "\n")
        
        # State for streaming output
        last_stream_agent_id: str | None = None
        stream_line_open: bool = False

        # Continuous conversation loop
        while True:
            try:
                user_query = input("You: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'bye', '']:
                    print("\n👋 Goodbye! Thanks for using the Finance RAG Agent!")
                    break
                if not user_query:
                    continue
                print("\n🔄 Processing your request...")
                # Run the workflow with user's query
                output: str | None = None
                async for event in workflow.run_stream(user_query):
                    if isinstance(event, AgentRunUpdateEvent):
                        props = event.data.additional_properties if event.data else None
                        event_type = props.get("magentic_event_type") if props else None

                        if event_type == MAGENTIC_EVENT_TYPE_ORCHESTRATOR:
                            kind = props.get("orchestrator_message_kind", "") if props else ""
                            text = event.data.text if event.data else ""
                            print(f"\n[🎯 Manager:{kind}]\n{text}\n{'-' * 50}")
                            
                        elif event_type == MAGENTIC_EVENT_TYPE_AGENT_DELTA:
                            agent_id = props.get("agent_id", event.executor_id) if props else event.executor_id
                            if last_stream_agent_id != agent_id or not stream_line_open:
                                if stream_line_open:
                                    print()
                                # Map agent IDs to emojis
                                agent_emoji = {
                                    "InvestmentAgent": "📊",
                                    "AdvisorAgent": "💰",
                                    "ResearchAgent": "📚"
                                }.get(agent_id, "🤖")
                                print(f"\n[{agent_emoji} {agent_id}]: ", end="", flush=True)
                                last_stream_agent_id = agent_id
                                stream_line_open = True
                            if event.data and event.data.text:
                                print(event.data.text, end="", flush=True)
                                
                        elif event.data and event.data.text:
                            print(event.data.text, end="", flush=True)
                            
                    elif isinstance(event, WorkflowOutputEvent):
                        output_messages = cast(list[ChatMessage], event.data)
                        if output_messages:
                            output = output_messages[-1].text

                if stream_line_open:
                    print()

                if output is not None:
                    print(f"\n{'='*70}")
                    print(f"✅ Final Response:\n\n{output}")
                    print(f"{'='*70}\n")
                else:
                    print("\n⚠️ No response generated. Please try rephrasing your question.\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error processing request: {str(e)}")
                logger.exception("Request processing error", exc_info=e)
                print("Please try again or type 'quit' to exit.\n")
                
    except Exception as e:
        print(f"\n❌ Initialization error: {str(e)}")
        logger.exception("Initialization error", exc_info=e)
    finally:
        # Cleanup
        try:
            await search_index_manager.close()
            await embeddings_client.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    asyncio.run(main())