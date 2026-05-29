import streamlit as st

from app.rag.qa_chain import ask_question
from app.voice.tts import text_to_audio
from app.voice.stt import speech_to_text


st.set_page_config(
    page_title="Arquitecto IA",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

if "pregunta" not in st.session_state:
    st.session_state["pregunta"] = ""

if "respuesta" not in st.session_state:
    st.session_state["respuesta"] = None

if "fuentes" not in st.session_state:
    st.session_state["fuentes"] = []

st.title("🤖 Sistema Inteligente de Trazabilidad de Software")

st.write("Puedes escribir tu pregunta o dictarla usando el micrófono.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎤 Dictar pregunta por voz"):
        st.info("Escuchando... habla ahora.")

        texto = speech_to_text()

        if texto:
            st.session_state["pregunta"] = texto
            st.success(f"Texto detectado: {texto}")
        else:
            st.warning("No se pudo reconocer la voz. Intenta de nuevo.")

with col2:
    if st.button("🧹 Limpiar pregunta"):
        st.session_state["pregunta"] = ""
        st.session_state["respuesta"] = None
        st.session_state["fuentes"] = []
        st.rerun()

with col3:
    if st.button("🗑️ Limpiar memoria"):
        st.session_state.history = []
        st.success("Memoria conversacional limpiada.")

question = st.text_input(
    "Haz una pregunta técnica",
    key="pregunta"
)

if st.button("🔎 Consultar"):

    if question.strip():

        result = ask_question(
            question,
            st.session_state.history
        )

        st.session_state["respuesta"] = result["response"]
        st.session_state["fuentes"] = result["sources"]

        st.session_state.history.append(
            {
                "question": question,
                "answer": result["response"]
            }
        )

    else:
        st.warning("Escribe o dicta una pregunta primero.")

if st.session_state["respuesta"]:

    st.subheader("Respuesta")
    st.markdown(st.session_state["respuesta"])

    st.subheader("🔊 Voz del asistente")

    if st.button("Generar audio de la respuesta"):

        audio_path = text_to_audio(st.session_state["respuesta"])

        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

    st.subheader("Fuentes")

    if st.session_state["fuentes"]:
        for source in st.session_state["fuentes"]:
            st.write(source)
    else:
        st.write("Sin fuentes disponibles.")

with st.expander("🧠 Ver memoria conversacional"):
    if st.session_state.history:
        for item in st.session_state.history:
            st.markdown(f"**Pregunta:** {item['question']}")
            st.markdown(f"**Respuesta:** {item['answer'][:500]}...")
            st.divider()
    else:
        st.write("Aún no hay memoria conversacional.")