import streamlit as st
from PIL import Image, ImageFilter
from rembg import remove
import io

st.set_page_config(page_title="Eliminador de Fondo", page_icon="🖼️", layout="wide")
st.title("✨ Eliminador de Fondo")
st.markdown("Sube tu foto y descárgala sin fondo al instante")

with st.sidebar:
    st.header("Ajustes")
    suavizado = st.slider("Suavizado de bordes", 0, 10, 1)
    tipo_fondo = st.selectbox("Fondo", ["Transparente", "Color sólido"])
    color_fondo = st.color_picker("Color de fondo", "#FFFFFF") if tipo_fondo == "Color sólido" else None

col1, col2 = st.columns(2)
with col1:
    st.subheader("Tu Imagen")
    archivo = st.file_uploader("Arrastra o selecciona", type=["png","jpg","jpeg","webp"])

def procesar(img, suav, fondo_tipo, color):
    sinf = remove(img)
    if suav > 0:
        alfa = sinf.split()[3].filter(ImageFilter.GaussianBlur(suav))
        sinf.putalpha(alfa)
    if fondo_tipo == "Color sólido" and color:
        nueva = Image.new("RGB", sinf.size, color)
        nueva.paste(sinf, mask=sinf.split()[3])
        return nueva
    return sinf

def descargar_imagen(img):
    buf = io.BytesIO()
    if img.mode == "RGBA":
        img.save(buf, format="PNG")
        return buf.getvalue(), "imagen_sin_fondo.png", "image/png"
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue(), "imagen_sin_fondo.jpg", "image/jpeg"

if archivo:
    original = Image.open(archivo)
    with col1: st.image(original, "Original", use_container_width=True)
    with st.spinner("Procesando..."):
        resultado = procesar(original, suavizado, tipo_fondo, color_fondo)
    with col2:
        st.subheader("Resultado ✅")
        st.image(resultado, use_container_width=True)
        datos, nom, mime = descargar_imagen(resultado)
        st.download_button("💾 Descargar", datos, nom, mime, type="primary")
    st.success("¡Listo! Descarga tu imagen arriba 👆")
else:
    st.info("👆 Sube una imagen para empezar")

