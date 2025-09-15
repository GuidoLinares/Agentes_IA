import speech_recognition as sr
from gtts import gTTS
import os 
import playsound


audio_file_counter = 0

def escuchar_microfono():
    """
    Captura audio del microfono y lo conviernes a texto
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Di algo...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language = 'es-ES')
        print(f"Acabas de decir:{texto}")
        return texto
    except sr.UnknownValueError:
        print("Lo siento, no entendi lo que dijiste")
        return None
    except sr.RequestError as e:
        print(f"Error en el servicio de reconocimiento de voz: {e}")


def hablar_texto(texto):
    """
    Convierte u texto a voz usando gTTS con acento de España y lo reproduce
    """


    global audio_file_counter
    try: 
        tts = gTTS(text = texto, lang='es', tld = 'es')
        audio_file = f"response_ {audio_file_counter}.mp3"
        tts.save(audio_file)
        audio_file_counter += 1
        print(f"Nexus dice: {texto}")
        playsound.playsound(audio_file)
        os.remove(audio_file)
    except Exception as e:
        print(f"Ocurrio un error al intentar hablar: {e}")
        
