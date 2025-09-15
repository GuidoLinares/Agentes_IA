import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carga las variables de entorno para las claves de API
load_dotenv()

# --- Funciones de las herramientas ---

def get_current_weather(city: str) -> str:
    """Obtiene el clima actual para una ciudad especificada usando OpenWeatherMap."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "ERROR. La clave API de openweather no fue encontrada"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        city_name = data["name"]
        weather_condition = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        return (f"El clima en {city_name} es: {weather_condition} con una temperatura de {temperature}°C "
                f"con una sensación térmica de {feels_like}°C y una humedad de {humidity}%.")
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return f"No se pudo encontrar la ciudad: {city}. Por favor, verifica el nombre."
        elif response.status_code == 401:
            return "Error de autenticación. Verifica tu clave de API de OpenWeatherMap."
        else:
            return f"Error HTTP: {http_err}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

def end_conversation() -> str:
    """Simula la finalización de la conversación."""
    return "El usuario ha terminado la conversación"

def get_current_datetime() -> str:
    """Devuelve la fecha y hora en un formato legible en español."""
    dias = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    meses = {
        "January": "enero",
        "February": "febrero",
        "March": "marzo",
        "April": "abril",
        "May": "mayo",
        "June": "junio",
        "July": "julio",
        "August": "agosto",
        "September": "septiembre",
        "October": "octubre",
        "November": "noviembre",
        "December": "diciembre"
    }
    try:
        now = datetime.now()
        fecha_formateada_en = now.strftime("%A, %d de %B de %Y, %H:%M")
        dia_en = now.strftime("%A")
        mes_en = now.strftime("%B")
        fecha_traducida = fecha_formateada_en.replace(dia_en, dias[dia_en]).replace(mes_en, meses[mes_en])
        return f"La fecha y hora actual es: {fecha_traducida}."
    except Exception as e:
        return f"Error al obtener la fecha y hora: {e}"

# --- Verificación de las herramientas ---

print("--- Verificando la herramienta get_current_weather ---")
# Prueba con una ciudad válida
print(f"Resultado para Buenos Aires: {get_current_weather('Buenos Aires')}")
# Prueba con una ciudad inválida para verificar el manejo de errores
print(f"Resultado para Ciudad_Inexistente: {get_current_weather('Ciudad_Inexistente')}")

print("\n--- Verificando la herramienta get_current_datetime ---")
# Prueba la herramienta de fecha y hora
print(f"Resultado: {get_current_datetime()}")

print("\n--- Verificando la herramienta end_conversation ---")
# Prueba la herramienta de finalización de conversación
print(f"Resultado: {end_conversation()}")

# --- Diagnóstico de la clave de API ---
api_key_status = os.getenv("OPENWEATHER_API_KEY")
print("\n--- Diagnóstico de la clave de API ---")
if api_key_status:
    print(f"Clave de API de OpenWeatherMap encontrada: {api_key_status[:4]}...{api_key_status[-4:]}")
else:
    print("La clave de API de OpenWeatherMap NO fue encontrada. Asegúrate de que tu archivo .env esté configurado correctamente.")