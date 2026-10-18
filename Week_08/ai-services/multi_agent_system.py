"""
Week 7 Part E: Multi-Agent Supervisor Architecture (Stretch Tier)
Implements:
1. Catalog Agent: Specialized read-only agent (search_catalog, check_availability). Enforces least privilege (no write tools).
2. Circulation Agent: Specialized write agent (reserve_book, list_my_reservations). Requires approval for reservations.
3. Supervisor Node: Orchestrator routing to Next(Literal["catalog_agent", "circulation_agent", "FINISH"]).
4. Global step limit: Hard ceiling to prevent infinite worker-supervisor ping-pong cycles.
"""

from typing import Annotated, TypedDict, List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agent_tools import search_catalog, check_availability, reserve_book, list_my_reservations, RISKY_TOOLS
from model_factory import get_chat_model

MAX_SUPERVISOR_STEPS = 6

# ---------------------------------------------------------------------------
# 1. Multi-Agent State Definition
# ---------------------------------------------------------------------------
class MultiAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next: str
    steps: int

# ---------------------------------------------------------------------------
# 2. Supervisor Schema & Prompts
# ---------------------------------------------------------------------------
class SupervisorDecision(BaseModel):
    next: Literal["catalog_agent", "circulation_agent", "FINISH"] = Field(
        description="The next specialized agent to call, or 'FINISH' if the user's objective is achieved or answered."
    )
    instruction: Optional[str] = Field(
        default=None,
        description="Specific directive for the chosen worker agent."
    )

SUPERVISOR_PROMPT = """You are the Library Multi-Agent Supervisor.
You manage two specialized worker agents:
1. 'catalog_agent': Responsible for searching book titles, authors, genres, and checking shelf availability. (Read-only, has NO reserve tools).
2. 'circulation_agent': Responsible for reserving books and viewing user loan records. (Handles all reservation writes).

Examine the conversation history and decide which worker should act next.
- If the user needs book recommendations, search, or availability checking, assign 'catalog_agent'.
- If the user wants to reserve a specific available book or check active reservations, assign 'circulation_agent'.
- Once the user's request has been fulfilled, answer clearly and output 'FINISH'."""

CATALOG_AGENT_PROMPT = """You are the Catalog Specialist.
You have tools: search_catalog, check_availability.
Your job is to look up books, find IDs, and confirm whether they are available.
Once you have retrieved the requested information, report your findings clearly and hand back control."""

CIRCULATION_AGENT_PROMPT = """You are the Circulation Specialist.
You have tools: reserve_book, list_my_reservations.
Your job is to reserve books on behalf of the user or show their current reservations.
Always ensure you have a valid book ID before reserving."""

# ---------------------------------------------------------------------------
# 3. Multi-Agent Graph Builder
# ---------------------------------------------------------------------------
def build_multi_agent_system(checkpointer: Optional[Any] = None):
    model = get_chat_model(temperature=0.0)

    # 1. Supervisor model
    supervisor_runnable = model.with_structured_output(SupervisorDecision)

    # 2. Worker models with strictly partitioned tool boundaries (Least Privilege)
    catalog_tools = [search_catalog, check_availability]
    circulation_tools = [reserve_book, list_my_reservations]

    catalog_model = model.bind_tools(catalog_tools)
    circulation_model = model.bind_tools(circulation_tools)

    # Supervisor Node
    def supervisor_node(state: MultiAgentState):
        messages = [SystemMessage(SUPERVISOR_PROMPT)] + state["messages"]
        decision: SupervisorDecision = supervisor_runnable.invoke(messages)
        return {
            "next": decision.next,
            "steps": state.get("steps", 0) + 1
        }

    # Catalog Agent Node
    def catalog_node(state: MultiAgentState, config: RunnableConfig):
        messages = [SystemMessage(CATALOG_AGENT_PROMPT)] + state["messages"]
        reply = catalog_model.invoke(messages, config)
        return {"messages": [reply]}

    # Circulation Agent Node
    def circulation_node(state: MultiAgentState, config: RunnableConfig):
        messages = [SystemMessage(CIRCULATION_AGENT_PROMPT)] + state["messages"]
        reply = circulation_model.invoke(messages, config)
        return {"messages": [reply]}

    # Conditional Routing Edge
    def route_supervisor(state: MultiAgentState):
        if state.get("steps", 0) >= MAX_SUPERVISOR_STEPS:
            return END
        next_worker = state.get("next", "FINISH")
        if next_worker == "FINISH":
            return END
        return next_worker

    # Build Graph
    builder = StateGraph(MultiAgentState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("catalog_agent", catalog_node)
    builder.add_node("catalog_tools", ToolNode(catalog_tools))
    builder.add_node("circulation_agent", circulation_node)
    builder.add_node("circulation_tools", ToolNode(circulation_tools))

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "catalog_agent": "catalog_agent",
            "circulation_agent": "circulation_agent",
            END: END
        }
    )

    # Worker inner loops
    def route_catalog_worker(state: MultiAgentState):
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return "catalog_tools"
        return "supervisor"

    def route_circulation_worker(state: MultiAgentState):
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            return "circulation_tools"
        return "supervisor"

    builder.add_conditional_edges("catalog_agent", route_catalog_worker, {"catalog_tools": "catalog_tools", "supervisor": "supervisor"})
    builder.add_edge("catalog_tools", "catalog_agent")

    builder.add_conditional_edges("circulation_agent", route_circulation_worker, {"circulation_tools": "circulation_tools", "supervisor": "supervisor"})
    builder.add_edge("circulation_tools", "circulation_agent")

    return builder.compile(checkpointer=checkpointer)
