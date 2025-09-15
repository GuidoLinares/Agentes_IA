import os
import requests
from langchain_core.tools import Tool
from datetime import datetime

def get_current_weather(city: str) -> str:
    """Obtiene el clima actual para una ciudad especificada usando OpenWeatherMap."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return ("ERROR. La clave API de openweather no fue encontrada")
    
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

weather_tool = Tool(
    name="get_current_weather",
    func=get_current_weather,
    description="Útil para obtener el clima actual en una ciudad específica. Recibe el nombre de la ciudad como entrada."
)

def end_conversation(input: str) -> str:
    """En esta función el usuario va a pedir finalizar la conversación"""
    return("El usuario ha terminado la conversación")

end_conversation_tool = Tool(
    name="end_conversation",
    func=end_conversation,
    description="Útil para finalizar una conversación con el usuario. Si pone palabras clave como chau o hasta luego, etc."
)


def get_current_datetime(input: str) -> str:
    """Devuelve la fecha y hora en un formato legible en español"""

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

current_datetime_tool = Tool(
    name="get_current_datetime",
    func=get_current_datetime,
    description="Útil para obtener la fecha y hora actual. Úsalo siempre que el usuario pregunte por 'hoy', 'mañana', 'ahora', o cualquier otra referencia temporal relativa al día o la hora actual."
)