from graph import build_graph
from config import graph_config


def run_chat_loop():
    graph = build_graph()

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit","exit","q"]:
                print("Goodbye!")
                break
            
            events = graph.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config = graph_config,
                stream_mode = "values"
            )

            final_event = None
            for event in events:
                final_event = event
                
            if final_event and "messages" in final_event:
                final_message = final_event["messages"][-1]
                
                if final_message.tool_calls:
                    
                    if final_message.tool_calls[0]['name'] == 'end_conversation':
                        print(f"AI: Ha sido un placer! Nos vemos.")
                        break
            
            if final_message.content:
                print(f"AI: {final_message.content}")


        except Exception as e:
            print(f"Ocurrio un error critico: {e}")
            break






