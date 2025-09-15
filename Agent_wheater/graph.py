from langgraph.graph import StateGraph,START, END
from langgraph.prebuilt import ToolNode,tools_condition
from config import tools,memory,llm_with_tools
from state import State


def router_function(state: State):
    """Revisa el ultimo mensaje: si contiene una llamada a una herramienta, 
    decide si es la herrameinta de salida o una herramienta normal"""

    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "end"
    
    if last_message.tool_calls[0].get("name") == "end_conversation":
        return "end"
    
    return "tools"


def build_graph() -> StateGraph:
    graph_builder = StateGraph(State)

    def chatbot(state:State):
        messages = llm_with_tools.invoke(state["messages"])
        return {"messages": [messages]}


    graph_builder.add_node("chatbot",chatbot)

    tool_node = ToolNode(tools)
    graph_builder.add_node("tools",tool_node)

    graph_builder.add_conditional_edges(
        "chatbot", 
        router_function,
        {
            "tools" : "tools",
            "end": END
        }
    )

    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")

    return graph_builder.compile(checkpointer=memory)




