# Script para verificar e instalar dependencias del agente de voz

import sys
import subprocess
import importlib.util

def check_package(package_name, import_name=None):
    """Verifica si un paquete está instalado"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    return spec is not None

def install_package(package_name):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

# Lista de dependencias necesarias
dependencies = {
    # Paquete pip : nombre para importar
    "langchain": "langchain",
    "langchain-google-genai": "langchain_google_genai",
    "langchain-tavily": "langchain_tavily", 
    "langgraph": "langgraph",
    "python-dotenv": "dotenv",
    "speechrecognition": "speech_recognition",
    "gtts": "gtts",
    "playsound": "playsound",
    "requests": "requests",
    "pyaudio": "pyaudio"  # Necesario para SpeechRecognition
}

print("🔍 Verificando dependencias...")
print("=" * 50)

missing_packages = []
installed_packages = []

for pip_name, import_name in dependencies.items():
    if check_package(pip_name, import_name):
        print(f"✅ {pip_name} - Instalado")
        installed_packages.append(pip_name)
    else:
        print(f"❌ {pip_name} - NO instalado")
        missing_packages.append(pip_name)

print("\n" + "=" * 50)
print(f"📊 Resumen: {len(installed_packages)} instalados, {len(missing_packages)} faltantes")

if missing_packages:
    print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
    print("\n🛠️  Para instalar todos los paquetes faltantes, ejecuta:")
    print(f"pip install {' '.join(missing_packages)}")
    
    # Instalación automática (opcional)
    auto_install = input("\n❓ ¿Deseas instalar automáticamente los paquetes faltantes? (s/n): ")
    if auto_install.lower() in ['s', 'si', 'y', 'yes']:
        print("\n📦 Instalando paquetes...")
        for package in missing_packages:
            print(f"Instalando {package}...")
            if install_package(package):
                print(f"✅ {package} instalado correctamente")
            else:
                print(f"❌ Error al instalar {package}")
else:
    print("\n🎉 ¡Todas las dependencias están instaladas!")

# Verificación específica para audio
print("\n🎤 Verificando configuración de audio...")
try:
    import speech_recognition as sr
    # Intentar listar micrófonos
    mic_list = sr.Microphone.list_microphone_names()
    if mic_list:
        print(f"✅ Audio OK - {len(mic_list)} micrófono(s) detectado(s)")
        print("🎯 Primer micrófono:", mic_list[0] if mic_list else "Ninguno")
    else:
        print("⚠️  No se detectaron micrófonos")
except Exception as e:
    print(f"❌ Error con audio: {e}")

# Verificación de variables de entorno
print("\n🔐 Verificando variables de entorno...")
import os
from dotenv import load_dotenv
load_dotenv()

env_vars = {
    "GOOGLE_API_KEY": "Google Gemini API",
    "OPENWEATHER_API_KEY": "OpenWeather API"
}

for var, description in env_vars.items():
    if os.getenv(var):
        print(f"✅ {var} - Configurada")
    else:
        print(f"❌ {var} - NO configurada ({description})")

print("\n" + "=" * 50)
print("🚀 Verificación completada!")