import streamlit as st
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

# Configuración de la paleta de colores
PRIMARY_COLOR = "#2F4858"
SECONDARY_COLOR = "#2C6974"
TERTIARY_COLOR = "#3C8B81"
HIGHLIGHT_COLOR = "#9FB869"

st.set_page_config(
    page_title="Proyecto EcoFriend",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Aplicación desarrollada para la presentación del proyecto SmartWaste."
    },
)

def set_custom_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: white;
            color: black;
        }}
        .stSidebar {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}
        .stButton>button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
        }}
        .stButton>button:hover {{
            background-color: {SECONDARY_COLOR};
        }}
        h1, h2, h3, h4, h5, h6, p {{
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Aplicar estilo personalizado
set_custom_style()

# Crear páginas
selected_page = st.sidebar.radio("Navegación", ["Inicio", "EcoFriend", "Dashboard", "Conócenos"], index=0)

if selected_page == "Inicio":
    st.markdown("<h1 style='text-align: center;'>Proyecto Smart Waste</h1>", unsafe_allow_html=True)
    st.image("Smartwaste_Streamlit/madrid-sol.jpg", use_container_width=True)
    st.markdown(
        f"""
        <p style="text-align:center;">

¡Hola a todos! Somos el equipo detrás de SmartWaste, un proyecto diseñado para mejorar la gestión de residuos en nuestra ciudad. Nuestro objetivo es hacer que la recolección de basura sea más eficiente, sostenible y adaptada a las necesidades de cada barrio.

Para ello, hemos analizado datos sobre la cantidad de residuos recogidos en distintos momentos del año y en diferentes zonas. Esto nos ha permitido descubrir patrones, entender qué distritos tienen un mejor desempeño y detectar oportunidades para optimizar el servicio.

Con SmartWaste, queremos contribuir a un entorno más limpio y ordenado, ayudando a que los recursos se utilicen de la mejor manera posible. ¡Porque una ciudad más sostenible es tarea de todos!

#SmartWaste #CuidemosNuestroEntorno #InnovaciónParaUnFuturoLimpio </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif selected_page == "EcoFriend":
    st.markdown(
        """
        <h1 style="text-align:center;">EcoFriend</h1>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("🔒 Ingrese su clave API de OpenAI para continuar")
    api_key = st.text_input("Clave API de OpenAI", type="password")

    if api_key:
        try:
            # Configurar OpenAI con la clave proporcionada
            openai.api_key = api_key

            # Cargar el modelo RAG
            @st.cache_resource
            def load_rag_model():
                try:
                    from langchain.vectorstores import Chroma
                    from langchain.embeddings.openai import OpenAIEmbeddings

                    # Asegúrese de que el índice se haya guardado previamente usando Chroma
                    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
                    vector_store = Chroma(persist_directory="/Users/jaquelinedicroce/Desktop/Bootcamp/Proyecto_Final_Smartwaste_Madrid/Smartwaste_Streamlit/vector_store", embedding_function=embeddings)
                    return vector_store
                except Exception as e:
                    st.error(f"Error al cargar el modelo RAG: {e}")
                    return None

            vector_store = load_rag_model()

            if vector_store:
                st.subheader("🤖 Haga una pregunta sobre el proyecto")
                query = st.text_area("Escribe tu pregunta aquí", "¿De qué trata este proyecto?")

                if st.button("Consultar"):
                    try:
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=ChatOpenAI(openai_api_key=api_key, temperature=0.7),
                            retriever=vector_store.as_retriever(),
                        )
                        response = qa_chain.run(query)
                        st.success("Respuesta:")
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error al realizar la consulta: {e}")
            else:
                st.warning("El modelo RAG no se pudo cargar. Por favor, recargue la página o contacte al soporte.")

        except Exception as e:
            st.error(f"Clave API inválida o error: {e}")
    else:
        st.info("Por favor, ingrese su clave API para comenzar.")

elif selected_page == "Dashboard":
    st.markdown("<h2 style='text-align: center;'>📊 Dashboard del Proyecto</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Resumen General", "Mapa de Distritos", "Residuos por Categoria", "Servicios de Limpieza"])
    with tab1:
        st.write('Este es resúmen de la recolección de residuos en Madrid los últimos tres años')
        st.components.v1.html(
            """
            <iframe title="SmartWaste_BI_2" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiODk3NjVmNTAtYTEyOC00MmY5LTgzZjAtZTZhOWIyYzgyNWZlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
            """,
            height=600,
        )

    with tab2:
            st.components.v1.html(
                """
                <iframe title="SmartWaste_BI_2" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiODk3NjVmNTAtYTEyOC00MmY5LTgzZjAtZTZhOWIyYzgyNWZlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9&pageName=46d13c11d01b639264b7" frameborder="0" allowFullScreen="true"></iframe>
                """,
                height=600,
            )

    with tab3:
            st.components.v1.html(
                """
                <iframe title="SmartWaste_BI_2" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiODk3NjVmNTAtYTEyOC00MmY5LTgzZjAtZTZhOWIyYzgyNWZlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9&pageName=0e4aae2400ec306d5025" frameborder="0" allowFullScreen="true"></iframe>
                """,
                height=600,
            )

    with tab4:
            st.components.v1.html(
                """
                <iframe title="SmartWaste_BI_2" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiODk3NjVmNTAtYTEyOC00MmY5LTgzZjAtZTZhOWIyYzgyNWZlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9&pageName=766999b24eaa1c546637" frameborder="0" allowFullScreen="true"></iframe>
                """,
                height=600,
            )

elif selected_page == "Conócenos":
    st.markdown("<h2 style='text-align: center;'>Conoce al Equipo</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:center;">
        <p style="text-align:center;">Con SmartWaste, hemos demostrado cómo el análisis de datos puede ayudar a mejorar la gestión de residuos en nuestra ciudad. Al identificar patrones y evaluar la eficiencia en distintos distritos, nuestro proyecto busca contribuir a un sistema de recolección más inteligente y sostenible.

Este ha sido un trabajo en equipo, y queremos agradecer a todos los que hicieron posible este proyecto.¡Gracias por acompañarnos en este recorrido! Sigamos trabajando juntos por una ciudad más limpia y eficiente. 🌍♻️</p>
        <p style="text-align:center;">Quienes somos:</p>
        <div style="display:flex;justify-content:center;">
            <div style="margin: 0 20px;">
                <img src="https://avatars.githubusercontent.com/u/109431439?v=4" alt="Inés Camerlynck" style="border-radius:50%;width:150px;height:150px;">
                <p>Inés Camerlynck</p>
                <p><a href="https://github.com/ICG216" target="_blank">GitHub</a></p>
            </div>
            <div style="margin: 0 20px;">
                <img src="https://avatars.githubusercontent.com/u/183011202?v=4" alt="Jaqueline Di Croce" style="border-radius:50%;width:150px;height:150px;">
                <p>Jaqueline Di Croce</p>
                <p><a href="https://github.com/jaquidicroce" target="_blank">GitHub</a></p>
            </div>
            <div style="margin: 0 20px;">
                <img src="https://avatars.githubusercontent.com/u/183004832?v=4" alt="Borja Cortés" style="border-radius:50%;width:150px;height:150px;">
                <p>Borja Cortés</p>
                <p><a href="https://github.com/borcdc" target="_blank">GitHub</a></p>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Footer
st.markdown(
    f"""
    <hr>
    <p style="text-align:center;color:black;">Desarrollado como parte del proyecto SmartWaste</p>
    """,
    unsafe_allow_html=True,
)
