from graph import build_graph
from config import graph_config

class Agente:
    """
    Clase que encapsula TODA la lógica del agente:
    - Construye el grafo.
    - Mantiene el historial de la conversación.
    - Procesa los mensajes.
    """
    def __init__(self):
        """
        Al crear el agente, automáticamente construye el grafo y prepara el historial.
        """
        self.graph = build_graph()
        
        self.historial_conversacion = []
        
        print("🤖 Agente con LangGraph inicializado y listo.")

    def procesar_turno(self, mensaje_usuario):
        """
        Esta función maneja un turno completo de la conversación.
        """
        self.historial_conversacion.append({"role": "user", "content": mensaje_usuario})

        try:
            events = self.graph.stream(
                {"messages": self.historial_conversacion},
                config=graph_config,
                stream_mode="values"
            )

            final_event = None
            for event in events:
                final_event = event
            
            if final_event and "messages" in final_event:
                mensaje_final_ai = final_event["messages"][-1]
                respuesta_texto = ""

                if mensaje_final_ai.tool_calls and mensaje_final_ai.tool_calls[0]['name'] == 'end_conversation':
                    respuesta_texto = "Ha sido un placer. ¡Nos vemos!"
                elif mensaje_final_ai.content:
                    respuesta_texto = mensaje_final_ai.content
                
                self.historial_conversacion.append(mensaje_final_ai)
                
                return respuesta_texto, (mensaje_final_ai.tool_calls and mensaje_final_ai.tool_calls[0]['name'] == 'end_conversation')

        except Exception as e:
            print(f"ERROR dentro del agente: {e}")
            return "Lo siento, ocurrió un error interno.", False