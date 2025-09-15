import os
import requests
from langchain_core.tools import Tool

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
                f"con una sensacion termica de {feels_like}°C y una humedad de {humidity}.")

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
    name = "get_current_weather",
    func = get_current_weather,
    description = "Util para obtener el clima actual e una ciudad específica. Recibe el nombre de la ciudad como entrada."
    )

def end_conversation(input: str) -> str:
    "En esta funcion el usuario va a pedir finalizar la conversacion"
    return("El usuario ha terminado la conversacion")
    
end_conversation_tool = Tool(
    name = "end_conversation",
    func = end_conversation,
    description="util para finalizar una conversacion con el usuario"
)



