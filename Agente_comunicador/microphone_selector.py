import speech_recognition as sr


def listar_y_seleccionar_microfono():
    """Lista todos los micrófonos disponibles y permite seleccionar uno"""
    print("🎤 Micrófonos disponibles:")
    print("=" * 60)
    
    mic_list = sr.Microphone.list_microphone_names()
    
    if not mic_list:
        print("❌ No se encontraron micrófonos.")
        return None
    
    # Mostrar todos los micrófonos
    for i, name in enumerate(mic_list):
        print(f"  [{i:2d}] {name}")
    
    print("=" * 60)
    print(f"Total: {len(mic_list)} micrófonos detectados")
    
    while True:
        try:
            seleccion = input(f"\n🎯 Selecciona el micrófono (0-{len(mic_list)-1}) o 'q' para salir: ").strip()
            
            if seleccion.lower() == 'q':
                return None
            
            indice = int(seleccion)
            
            if 0 <= indice < len(mic_list):
                nombre_mic = mic_list[indice]
                print(f"\n✅ Micrófono seleccionado: [{indice}] {nombre_mic}")
                
                # Probar el micrófono seleccionado
                confirmar = input("¿Quieres probarlo? (s/n): ").strip().lower()
                if confirmar in ['s', 'si', 'y', 'yes']:
                    if probar_microfono(indice, nombre_mic):
                        return indice
                    else:
                        print("❌ El micrófono no funcionó correctamente.")
                        continue
                else:
                    return indice
            else:
                print(f"❌ Número inválido. Debe estar entre 0 y {len(mic_list)-1}")
                
        except ValueError:
            print("❌ Por favor ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n🚫 Operación cancelada.")
            return None

def probar_microfono(indice, nombre):
    """Prueba un micrófono específico"""
    print(f"\n🧪 Probando micrófono: {nombre}")
    print("📢 Di algo en los próximos 5 segundos...")
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=indice) as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎧 Escuchando...")
            
            # Escuchar por 5 segundos máximo
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
        print("🔄 Procesando audio...")
        texto = r.recognize_google(audio, language='es-ES')
        
        print(f"✅ ¡Funcionó! Detecté: '{texto}'")
        return True
        
    except sr.WaitTimeoutError:
        print("⏱️  Tiempo agotado - no se detectó audio")
        return False
    except sr.UnknownValueError:
        print("❓ No se pudo entender el audio, pero el micrófono funciona")
        return True  # El micrófono funciona, solo no entendió
    except sr.RequestError as e:
        print(f"❌ Error en el servicio de reconocimiento: {e}")
        return False
    except Exception as e:
        print(f"❌ Error con el micrófono: {e}")
        return False

def guardar_configuracion_microfono(indice):
    """Guarda la configuración del micrófono en un archivo"""
    try:
        with open('.microfono_config.txt', 'w') as f:
            f.write(str(indice))
        print(f"💾 Configuración guardada: micrófono índice {indice}")
    except Exception as e:
        print(f"❌ Error al guardar configuración: {e}")

def cargar_configuracion_microfono():
    """Carga la configuración del micrófono desde archivo"""
    try:
        with open('.microfono_config.txt', 'r') as f:
            indice = int(f.read().strip())
        print(f"📁 Configuración cargada: micrófono índice {indice}")
        return indice
    except FileNotFoundError:
        print("📁 No hay configuración previa guardada")
        return None
    except Exception as e:
        print(f"❌ Error al cargar configuración: {e}")
        return None

if __name__ == "__main__":
    print("🎤 CONFIGURADOR DE MICRÓFONO")
    print("=" * 40)
    
    # Intentar cargar configuración previa
    indice_previo = cargar_configuracion_microfono()
    if indice_previo is not None:
        mic_list = sr.Microphone.list_microphone_names()
        if 0 <= indice_previo < len(mic_list):
            print(f"🔄 Configuración previa encontrada: [{indice_previo}] {mic_list[indice_previo]}")
            usar_previo = input("¿Usar esta configuración? (s/n): ").strip().lower()
            if usar_previo in ['s', 'si', 'y', 'yes']:
                print("✅ Usando configuración previa")
                exit()
    
    # Seleccionar nuevo micrófono
    indice_seleccionado = listar_y_seleccionar_microfono()
    
    if indice_seleccionado is not None:
        guardar_configuracion_microfono(indice_seleccionado)
        print(f"\n🎉 ¡Listo! Ahora tu aplicación usará el micrófono índice {indice_seleccionado}")
        print("💡 Tip: Puedes ejecutar este script cuando quieras cambiar de micrófono")
    else:
        print("🚫 No se seleccionó ningún micrófono")