from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.error_agent import error_summarize_agent
from agents.error_email_agent import handle_error


class ErrorState(TypedDict, total=False):

    timestamp: str
    response_type: str
    response_json: str

    error_summary: dict
    significance: str
    mail_result: str


def error_summarizer(state: ErrorState):

    incident = [{
        "timestamp": state["timestamp"],
        "Response_type": state["response_type"],
        "Response_json": state["response_json"]
    }]

    result = error_summarize_agent(incident)

    return {
        "error_summary": result,
        "significance": result["severity"]
    }


def route_error(state: ErrorState):

    if state["significance"] in [
        "CRITICAL",
        "WARNING"
    ]:
        return "handle_error"

    return "end"


def handle_error_node(state: ErrorState):

    result = handle_error.invoke({
        "error_summary": str(
            state["error_summary"]
        )
    })

    return {
        "mail_result": result
    }


graph = StateGraph(ErrorState)

graph.add_node(
    "summarize_error",
    error_summarizer
)

graph.add_node(
    "handle_error",
    handle_error_node
)

graph.add_edge(
    START,
    "summarize_error"
)

graph.add_conditional_edges(
    "summarize_error",
    route_error,
    {
        "handle_error": "handle_error",
        "end": END
    }
)

graph.add_edge(
    "handle_error",
    END
)

error_workflow = graph.compile()