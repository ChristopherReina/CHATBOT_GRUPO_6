import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")


# Cargar la API key de forma segura
# Cargar la API key de forma segura
load_dotenv()  # No falla si .env no existe
API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
if not API_KEY:
    st.error("Falta GROQ_API_KEY en .env o en st.secrets.")
    st.stop()

client = Groq(api_key=API_KEY)
  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = "Eres un asistente virtual amable llamado Conovator y experto en ventas B2B de nuestro dispositivo" \
" de detección de somnolencia para el sector de transporte interprovincial, turístico, minería e " \
"internacional. Tu principal tarea es asesorar a las empresas de transporte sobre la adquisición de" \
"nuestro dispositivo mediante nuestra página web. " \
"Características de nuestro producto:" \
"- Precio de 850 soles por unidad" \
"- Componentes: Cámara, raspberry pi, carcasa para ubicar en los buses, aplicación de telemetría que " \
" permite que los buses se conecten a la central de la empresa para monitoreo en tiempo real y control de las alertas" \
"- planes: 1ro: suscripción de 5 años y actualizaciones constantes totalmente gratuitas, 2do: suscripción de 3 años y" \
"mantenimientos preventivos cada 3 meses." \
"Explica al cliente cómo el dispositivo detecta la somnolencia en carreteras de madrugada y por qué resulta más seguro y" \
" económico que contratar dos choferes por turno, destacando su sistema basado en PERCLOS, que mide el porcentaje de cierre " \
"en los parpadeos y ha sido validado por la Federal Highway Administration (FHWA) y gestionado por la National Highway Traffic Safety Administration (NHTSA) como el indicador más confiable para detectar somnolencia en conductores; enfatiza cómo su implementación masiva puede salvar vidas y reducir accidentes en las carreteras, menciona que el dispositivo cumple con las regulaciones peruanas de transporte y salud, invita siempre a una reunión de demostración gratuita del dispositivo, y añade que la tecnología se actualizará con inteligencia artificial para reconocer patrones de fatiga más avanzados en el futuro."

st.title("🤖 Chatbot Conovator")
st.write("Holaaa!! Soy conovator, estoy aquí para ayudarte a resolver todas tus dudas y ser tu asesor de compra.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.extend(st.session_state.chat_history)

    # Llamar a la API **solo** si hay user_input (evita NameError)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content  # objeto, no dict
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})




