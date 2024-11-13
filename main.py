import streamlit as st
from groq import Groq

st.set_page_config(
    page_title = "ChatBot",
    page_icon = "logoIA.png",
    layout = "centered"
)

#st.title("Aplicacion con streamlit")

#name = st.text_input("¿Cual es tu nombre?: ")

#if st.button("Saludo"):
#    st.write(f"Hola {name}, un saludos!")

version = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def config() :
    st.title("Mi chat con Inteligencia Artificial")
    st.sidebar.title("Configuracion de IA")
    opcionModelo = st.sidebar.selectbox(
        "Modelo: ",
        options = version,
        index = 0
    )
    return opcionModelo

def usuarioGroq() :
    secretKey = st.secrets["SECRET_KEY"]
    return Groq(api_key = secretKey)

def configModelo(cliente, modelo, mensajeInput) :
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role": "user", "content": mensajeInput}],
        stream = True
    )

def inicializadorEstado() :
    if "mensajes" not in st.session_state :
        st.session_state.mensajes = []

def actualizarHistorial(rol, contenido, avatar) :
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrarHistorial() :
    for mensaje in st.session_state.mensajes :
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]) :
            st.markdown(mensaje["content"])

def areaChat() :
    contenedor = st.container(height = 300, border = True)
    with contenedor :
        mostrarHistorial()

def respuestaChat(chat) :
    respuesta = ""
    for frase in chat :
        if frase.choices[0].delta.content :
            respuesta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return frase

def main() :
    modelo = config()
    cliente = usuarioGroq()
    inicializadorEstado()
    areaChat()
    mensaje = st.chat_input("¿Con que lo ayudamos hoy?")
    if mensaje :
        actualizarHistorial("user", mensaje, "🗣️")
        chat = configModelo(cliente, modelo, mensaje)

        if chat :
            with st.chat_message("assistant") :
                respuesta = st.write_stream(respuestaChat(chat))
                actualizarHistorial("assistant", respuesta, "🦚")

                st.rerun()

if __name__ == "__main__" :
    main()