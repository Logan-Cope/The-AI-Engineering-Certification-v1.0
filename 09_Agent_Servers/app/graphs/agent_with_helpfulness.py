from __future__ import annotations

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from app.graphs.simple_agent import SYSTEM_PROMPT
from app.models import get_chat_model
from app.tools import get_tool_belt

# Safety limit: stop looping once the conversation grows past this many messages,
# so a response the judge never likes can't retry forever.
MAX_MESSAGES = 10


def call_model(state: MessagesState) -> dict:
    model = get_chat_model().bind_tools(get_tool_belt())
    messages = [("system", SYSTEM_PROMPT), *state["messages"]]
    return {"messages": [model.invoke(messages)]}


def route_after_agent(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "action"
    return "helpfulness"


_helpfulness_prompt = ChatPromptTemplate.from_template(
    "Given an initial query and a final response, determine if the final response "
    "is extremely helpful or not. Respond with only Y or N.\n\n"
    "Initial Query:\n{initial_query}\n\n"
    "Final Response:\n{final_response}"
)


def helpfulness_node(state: MessagesState) -> dict:
    if len(state["messages"]) > MAX_MESSAGES:
        return {"messages": [AIMessage(content="HELPFULNESS:END")]}

    initial_query = state["messages"][0].content
    final_response = state["messages"][-1].content

    chain = _helpfulness_prompt | get_chat_model() | StrOutputParser()
    result = chain.invoke(
        {"initial_query": initial_query, "final_response": final_response}
    )

    decision = "Y" if result.strip().upper().startswith("Y") else "N"
    return {"messages": [AIMessage(content=f"HELPFULNESS:{decision}")]}


def helpfulness_decision(state: MessagesState) -> str:
    last_text = getattr(state["messages"][-1], "content", "")
    if "HELPFULNESS:END" in last_text:
        return "end"
    if "HELPFULNESS:Y" in last_text:
        return "end"
    return "continue"


def build_graph():
    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("action", ToolNode(get_tool_belt()))
    graph.add_node("helpfulness", helpfulness_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        route_after_agent,
        {"action": "action", "helpfulness": "helpfulness"},
    )
    graph.add_edge("action", "agent")
    graph.add_conditional_edges(
        "helpfulness",
        helpfulness_decision,
        {"continue": "agent", "end": END},
    )
    return graph


graph = build_graph().compile()
