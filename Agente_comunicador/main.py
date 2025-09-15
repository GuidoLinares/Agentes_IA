from app import Agente
from audio_handler import escuchar_microfono, hablar_texto

def main():
    """
    Función principal que solo se encarga de la interfaz de voz.
    Toda la lógica compleja vive dentro del Agente.
    """
    agente = Agente()

    hablar_texto("Hola, soy Nexus. ¿Cómo puedo ayudarte?")

    while True:
        mensaje_usuario = escuchar_microfono()

        if mensaje_usuario is None:
            continue
        
        respuesta_texto, debe_terminar = agente.procesar_turno(mensaje_usuario)
        
        hablar_texto(respuesta_texto)

        if debe_terminar:
            break

if __name__ == "__main__":
    main()