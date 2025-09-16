import speech_recognition as sr
from gtts import gTTS
import os 
import playsound

audio_file_counter = 0

def cargar_microfono_configurado():
    """Carga el índice del micrófono configurado"""
    try:
        with open('.microfono_config.txt', 'r') as f:
            indice = int(f.read().strip())
        
        # Verificar que el índice sea válido
        mic_list = sr.Microphone.list_microphone_names()
        if 0 <= indice < len(mic_list):
            print(f"🎤 Usando micrófono configurado: [{indice}] {mic_list[indice]}")
            return indice
        else:
            print(f"⚠️  Índice de micrófono inválido ({indice}), usando por defecto")
            return None
            
    except FileNotFoundError:
        print("📁 No hay configuración de micrófono. Ejecuta 'python microphone_selector.py' para configurar")
        return None
    except Exception as e:
        print(f"❌ Error al cargar configuración de micrófono: {e}")
        return None

def escuchar_microfono():
    """
    Captura audio del micrófono configurado y lo convierte a texto
    """
    r = sr.Recognizer()
    
    indice_mic = cargar_microfono_configurado()
    
    try:
        if indice_mic is not None:
            with sr.Microphone(device_index=indice_mic) as source:
                print(f"🎤 Di algo...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10, phrase_time_limit=8)
        else:
            with sr.Microphone() as source:
                print(f"🎤 Di algo (micrófono por defecto)...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10, phrase_time_limit=8)
    
        texto = r.recognize_google(audio, language='es-MX')
        print(f"✅ Acabas de decir: {texto}")
        return texto
        
    except sr.WaitTimeoutError:
        print("⏱️  Tiempo agotado - no se detectó voz")
        return None
    except sr.UnknownValueError:
        print("❓ Lo siento, no entendí lo que dijiste")
        return None
    except sr.RequestError as e:
        print(f"❌ Error en el servicio de reconocimiento de voz: {e}")
        return None
    except Exception as e:
        print(f"❌ Error general con el micrófono: {e}")
        print("💡 Tip: Ejecuta 'python microphone_selector.py' para reconfigurar")
        return None

def hablar_texto(texto):
    """
    Convierte un texto a voz usando gTTS con acento de España y lo reproduce
    """
    global audio_file_counter
    try: 
        tts = gTTS(text=texto, lang='es', tld='es')
        audio_file = f"response_{audio_file_counter}.mp3"
        tts.save(audio_file)
        audio_file_counter += 1
        
        print(f"🤖 Nexus dice: {texto}")
        playsound.playsound(audio_file)
        
        # Limpiar archivo temporal
        os.remove(audio_file)
        
    except Exception as e:
        print(f"❌ Ocurrió un error al intentar hablar: {e}")

def listar_microfonos():
    """Imprime una lista de los micrófonos disponibles y sus índices."""
    mic_list = sr.Microphone.list_microphone_names()
    if not mic_list:
        print("❌ No se encontraron micrófonos disponibles.")
        return

    print("🎤 Micrófonos disponibles:")
    print("=" * 50)
    for i, name in enumerate(mic_list):
        # Marcar el micrófono configurado
        marca = " ⭐" if es_microfono_configurado(i) else ""
        print(f"  [{i:2d}] {name}{marca}")
    
    print("=" * 50)
    print(f"Total: {len(mic_list)} micrófonos")
    print("⭐ = Micrófono configurado actualmente")

def es_microfono_configurado(indice):
    """Verifica si un índice es el micrófono configurado"""
    try:
        with open('.microfono_config.txt', 'r') as f:
            indice_config = int(f.read().strip())
        return indice == indice_config
    except:
        return False

def mostrar_microfono_actual():
    """Muestra qué micrófono está configurado actualmente"""
    indice = cargar_microfono_configurado()
    if indice is not None:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"🎤 Micrófono actual: [{indice}] {mic_list[indice]}")
    else:
        print("🎤 Usando micrófono por defecto (no configurado)")

# Mostrar configuración actual al importar el módulo
if __name__ == "__main__":
    listar_microfonos()
else:
    mostrar_microfono_actual()