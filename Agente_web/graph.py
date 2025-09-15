from langgraph.graph import StateGraph,START, END
from langgraph.prebuilt import ToolNode,tools_condition
from config import tools,memory,llm_with_tools
from state import State
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


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

    prompt_with_tools = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil que usa herramientas para obtener información cuando el usuario lo necesita. Responde de la mejor manera posible a las preguntas del usuario usando las herramientas disponibles. Si no hay una herramienta para la pregunta, responde directamente. Nunca te disculpes por no poder responder, siempre intenta encontrar una solución."),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = prompt_with_tools | llm_with_tools

    def chatbot(state:State):
        messages = chain.invoke({"messages": state["messages"]})
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


