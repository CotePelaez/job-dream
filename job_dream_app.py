import streamlit as st
from openai import OpenAI
import PyPDF2
import os


button_style = """
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        background-color: #FFA07A;
        color: white;
        font-size: 20px;
        border-radius: 10px;
        border: none;
    }
    </style>
    """

# Inyectar el CSS en la app
st.markdown(button_style, unsafe_allow_html=True)

# URL de la imagen
image_url = "fondo.jpeg"
image_solution = "tuanalisis.jpeg"

# Configuración del encabezado con la imagen desde la URL
st.image(image_url, use_column_width=True)

# Opcional: Título o descripción debajo de la imagen
st.title("Análisis de CV y Ofertas de Trabajo")
st.subheader("Personaliza tu CV y prepárate para tu entrevista de forma efectiva.")

# Configuración de la API de OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

# Función para leer archivos PDF usando PyPDF2
def read_pdf(uploaded_file):
    try:
        # Crear un lector de PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        # Extraer texto de cada página
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None

# Subida de archivos
cv_file = st.file_uploader('Sube tu CV (PDF, DOCX, etc.)', type=['txt', 'pdf', 'docx', 'doc', 'odt'])
job_file = st.file_uploader('Sube la oferta de trabajo (PDF, DOCX, etc.)', type=['txt', 'pdf', 'docx', 'doc', 'odt'])


# Verificar si ambos archivos han sido cargados
if cv_file and job_file:
    # Leer los archivos usando PyPDF2 (aquí podrías agregar soporte para otros tipos de archivos)
    cv_text = read_pdf(cv_file)
    job_text = read_pdf(job_file)


    if ((cv_text) and (job_text)):
        # Mostrar los primeros 1000 caracteres del CV y la oferta de trabajo para verificar su contenido
        #st.subheader('Texto extraído del Currículum:')
        #st.text(cv_text[:100])  # Muestra los primeros 1000 caracteres

        #st.subheader('Texto extraído de la Oferta de Trabajo:')
        #st.text(job_text[:100])  # Muestra los primeros 1000 caracteres

        # Verificar si el texto extraído es legible
        if len(cv_text) > 0 and len(job_text) > 0:
            # Generar el prompt para OpenAI
            prompt = f"""
            Contexto:
            Tienes un currículum guardado y una oferta de trabajo. Necesitas evaluar la adecuación entre el perfil del candidato y la oferta de trabajo, optimizar el currículum y preparar al candidato para la entrevista.

            Tarea:
            1. Realizar un análisis DAFO (fortalezas, debilidades, oportunidades y amenazas) entre el currículum del candidato y la oferta de trabajo y mostrarlo en una tabla
            2. Proporcionar sugerencias específicas para ajustar y cambiar el CV y alinearlo mejor con la oferta.
            3. Dar pautas claras para que el candidato se prepare adecuadamente para la entrevista.

            Currículum del candidato:
            {cv_text}

            Descripción de la oferta de trabajo:
            {job_text}

            Instrucción:
            Primero, realiza el análisis DAFO. Luego, da sugerencias detalladas para modificar el CV del candidato y ajustarlo mejor a los requisitos del puesto. Finalmente, brinda recomendaciones para la entrevista.

            Formato de la respuesta:
            - DAFO (en negrita y mas grande)
            añade una linea de color rosa claro
            - Sugerencias de ajuste (en negrita y mas grande)
             añade una linea de color rosa claro
            - Recomendaciones para la entrevista (en negrita y mas grande)

    
            """
            # Llamada a la API de OpenAI
            try:
                if st.button("Realizar análisis"):
                    client = OpenAI(api_key= openai_api_key)    
                    respuesta = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        max_tokens=4000,  # Ajustar el límite de tokens según la necesidad
                        temperature=0.4,
                        messages=[{'role': 'user', 'content': prompt}]
                    )
                    assesment = respuesta.choices[0].message.content
                    # Mostrar el análisis
                    st.image(image_solution, use_column_width=True)
                    st.subheader("Aquí va el análisis hecho por la IA:")
                    st.write(assesment)
            except Exception as e:
                st.error(f"Error al llamar a la API de OpenAI: {e}")
        else:
            st.error("El texto extraído no es válido o no se pudo extraer correctamente.")
    else:
        st.error("No se pudo extraer el texto de los archivos.")
