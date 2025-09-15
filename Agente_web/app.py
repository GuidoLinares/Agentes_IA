from graph import build_graph
from config import graph_config
import streamlit as st

@st.cache_resource
def load_graph():
    return build_graph()

graph = load_graph()

st.title("Charlie Asistente IA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("En que puedo ayudarte?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_placeholder.markdown("Pensando... 🤔")

        try:
            events = graph.stream(
                {"messages": st.session_state.messages},
                config=graph_config,
                stream_mode="values"
            )

            final_event = None
            for event in events:
                final_event = event

            print("--- Final Event Received ---")
            print(final_event)
            print("--------------------------")

            if final_event and "messages" in final_event and final_event["messages"]:
                final_message = final_event["messages"][-1]
                assistant_response = ""
                
                is_end_conversation = False
                if final_message.tool_calls:
                    for tool_call in final_message.tool_calls:
                        if tool_call['name'] == 'end_conversation':
                            is_end_conversation = True
                            break
                        
                if final_message.tool_calls and final_message.tool_calls[0]['name'] == 'end_conversation':
                    assistant_response = "Ha sido un placer! Nos vemos."
                
                elif final_message.content:
                    assistant_response = final_message.content

                else:
                    assistant_response = "Lo siento, no pude procesar una respuesta. Intenta de nuevo."
                    print("DEBUG: El mensaje final estaba vacío o tenía una estructura inesperada:", final_message)


                response_placeholder.markdown(assistant_response)
                if assistant_response != "Lo siento, no pude procesar una respuesta. Intenta de nuevo.":
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            else:
                response_placeholder.markdown("Ocurrió un error al procesar la respuesta.")
                st.error("El evento final del grafo no contenía la clave 'messages' o estaba vacío.")
                print("DEBUG: El evento final no tenía el formato esperado:", final_event)

        except Exception as e:
            response_placeholder.markdown("Hubo un error crítico.")
            st.error(f"Se produjo una excepción: {e}")
            print(f"ERROR: Excepción durante graph.stream: {e}")