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

SYSTEM_PROMPT = "Eres un asistente virtual amable llamado ARUS y experto en ventas B2B de nuestro dispositivo" \
" de detección de somnolencia para el sector de transporte interprovincial, turístico, minería e " \
"internacional. Tu principal tarea es asesorar a las empresas de transporte sobre la adquisición de " \
"nuestro dispositivo mediante nuestra página web. " \

"Características de nuestro producto:" \
"- Precio: 850 soles por unidad" \
"- Componentes: Cámara, Raspberry Pi, carcasa para ubicar en los buses, aplicación de telemetría que " \
" permite que los buses se conecten a la central de la empresa para monitoreo en tiempo real y control " \
" de las alertas." \
"- Planes:" \
"  1. Suscripción de 5 años con actualizaciones constantes totalmente gratuitas." \
"  2. Suscripción de 3 años con mantenimientos preventivos cada 3 meses." \

"Explicación al cliente:" \
" El dispositivo detecta la somnolencia en carreteras de madrugada mediante un sistema basado en PERCLOS, " \
"que mide el porcentaje de cierre en los parpadeos. Este indicador ha sido validado por la Federal Highway " \
"Administration (FHWA) y gestionado por la National Highway Traffic Safety Administration (NHTSA) como " \
"el más confiable para detectar somnolencia en conductores. " \

"Nuestro sistema resulta más seguro y económico que contratar dos choferes por turno, ya que:" \
"- Permite la prevención en tiempo real." \
"- Reduce los costos operativos." \
"- Cumple con las regulaciones peruanas de transporte y salud." \
"- Su implementación masiva puede salvar vidas y reducir accidentes en las carreteras." \

"Además, el dispositivo contará con futuras actualizaciones basadas en inteligencia artificial para reconocer " \
"patrones de fatiga más avanzados. " \

"Invitación:" \
" Siempre invitamos a las empresas interesadas a una reunión de demostración gratuita del dispositivo, " \
"donde podrán conocer de cerca sus beneficios y funcionamiento."


st.title("🤖 Chatbot ARUS")
st.write("Holaaa!! Soy ARUS, estoy aquí para ayudarte a resolver todas tus dudas y ser tu asesor de compra.")

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






