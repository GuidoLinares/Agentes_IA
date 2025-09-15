from google import genai

client = genai.Client(api_key="AIzaSyBlZovExHExUgCvgX1RJJgxA4rZYTLalhI")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="podes explicarme en 5 pasos como funciona la rueda de un automovil"
)
print(response.text)





