import streamlit as st
import http.client
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import feedparser
from sklearn.linear_model import LinearRegression
import numpy as np
import requests
from bs4 import BeautifulSoup
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import itertools

# Configurar la página
st.set_page_config(page_title="💵 Precio del dólar Hoy", page_icon="💵", layout="wide")

@st.cache_data
## Predicciones

def actualizar_datos_blue():
    """Actualiza el archivo Bluex12.csv con el precio más reciente del dólar blue."""
    try:
        df = pd.read_csv("Bluex12.csv", encoding="utf-8")
        df['category'] = pd.to_datetime(df['category'], errors='coerce')
        df.set_index('category', inplace=True)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['category', 'valor'])
    except Exception as e:
        st.error(f"Error al cargar el archivo de datos: {e}")
        return
    
    # Obtener el precio actual del dólar blue
    datos = obtener_precio_dolar("blue")
    if "venta" in datos:
        nuevo_valor = datos["venta"]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verificar si ya se registró el valor del día
        if not df.empty and fecha_actual[:10] in df.index.strftime('%Y-%m-%d').values:
            st.info("Los datos ya están actualizados para hoy.")
        else:
            nuevo_registro = pd.DataFrame({"category": [fecha_actual], "valor": [nuevo_valor]})
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            df.to_csv("Bluex12.csv", index=False, encoding="utf-8")
            st.success("Datos del dólar blue actualizados correctamente.")
    else:
        st.warning("No se pudo obtener el precio del dólar blue.")

def obtener_datos_scraping():
    """Obtiene los datos históricos del dólar blue desde Dólar Hoy."""
    url = "https://dolarhoy.com/historico-dolar-blue#"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tabla = soup.find("table")
        
        if tabla:
            df = pd.read_html(str(tabla))[0]
            df.columns = ["Fecha", "Compra", "Venta"]
            df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")
            df.set_index("Fecha", inplace=True)
            df["Venta"] = pd.to_numeric(df["Venta"].str.replace("$", "").str.replace(",", ""), errors="coerce")
            return df
    
    return None

def predecir_dolar_blue(df, dias_prediccion):
    """Predice el valor del dólar blue usando ARIMA."""
    df = df.sort_index()
    serie = df['Venta']
    modelo = ARIMA(serie, order=(1,1,1))
    modelo_fit = modelo.fit()
    predicciones = modelo_fit.forecast(steps=dias_prediccion)
    fechas_prediccion = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=dias_prediccion, freq='D')
    df_predicciones = pd.DataFrame({'Fecha': fechas_prediccion, 'Predicción valor': predicciones})
    return df_predicciones

def mostrar_prediccion():
    st.title("📈 Predicción del Dólar Blue")
    df = obtener_datos_scraping()
    if df is not None and not df.empty:
        dias_prediccion = st.selectbox("Seleccione el horizonte de predicción (días):", [3, 6, 12, 24, 36])
        df_predicciones = predecir_dolar_blue(df, dias_prediccion)
        st.subheader(f"Predicción para los próximos {dias_prediccion} días")
        st.dataframe(df_predicciones)
        fig = px.line(df_predicciones, x='Fecha', y='Predicción valor', title=f"Predicción del Dólar Blue a {dias_prediccion} días")
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudieron obtener los datos históricos para realizar la predicción.")
def obtener_precio_dolar(tipo):
    """Obtiene el precio del dólar desde la API con manejo de errores y caché."""
    try:
        conn = http.client.HTTPSConnection("dolarapi.com")
        conn.request("GET", f"/v1/dolares/{tipo}")
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        return {"error": f"Error al obtener datos: {e}"}

# Diccionario con los tipos de dólar
tipos_dolar = {
    "Mayorista": "mayorista",
    "Oficial": "oficial",
    "MEP": "bolsa",
    "CCL": "contadoconliqui",
    "Cripto": "cripto",
    "Blue": "blue",
    "Tarjeta": "tarjeta"
}

def mostrar_precios():
    st.title("💵 Precio del dólar Hoy")
    
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))
    
    if st.button("🔄 Actualizar Precio"):
        datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])
        st.session_state[f"precio_{tipo_dolar}"] = datos  # Guardar en la sesión
    
    datos = st.session_state.get(f"precio_{tipo_dolar}", obtener_precio_dolar(tipos_dolar[tipo_dolar]))
    
    if "compra" in datos and "venta" in datos:
        compra = datos["compra"]
        venta = datos["venta"]
        
        st.markdown(
            f"""
            <div style="
                background-color: #222831;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: white;
            ">
                <span style="color: #33FF57;">💰 Compra: ${compra}</span><br>
                <span style="color: #FF5733;">📈 Venta: ${venta}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            📅 **Última actualización:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}  
            📌 **Fuente:** [DolarAPI](https://dolarapi.com)
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"⚠️ No se pudo obtener el precio del dólar {tipo_dolar}.")

## VARIACIONESSSSSSS
def mostrar_variacion():
    st.title("📊 Variación de Cotizaciones respecto al Oficial")

    precios = {}

    for nombre, tipo in tipos_dolar.items():
        datos = obtener_precio_dolar(tipo)
        if "venta" in datos:
            precios[nombre] = datos["venta"]
    
    if "Oficial" in precios:
        oficial = precios["Oficial"]
        variaciones = {nombre: ((precio / oficial) - 1) * 100 for nombre, precio in precios.items() if precio}

        df_variaciones = pd.DataFrame({
            "Tipo de Dólar": list(variaciones.keys()),
            "Variación %": list(variaciones.values()),
            "Precio": [precios[nombre] for nombre in variaciones.keys()]
        })

        # Crear el gráfico
        fig = px.scatter(
            df_variaciones,
            x="Precio",
            y="Tipo de Dólar",
            size="Precio",
            color="Variación %",
            text="Precio",
            hover_data=["Variación %"],
            title="Variación de Cotizaciones respecto al Dólar Oficial",
            size_max=15,
            color_continuous_scale=px.colors.sequential.Viridis
        )

        fig.update_layout(
            xaxis_title="Precio en $", 
            yaxis_title="Tipo de Dólar"
        )

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ No se pudo obtener el precio del Dólar Oficial.")


def convertir_monedas():
    st.title("💱 Convertidor de Moneda")
    tipo_dolar = st.selectbox("Seleccione el tipo de dólar:", list(tipos_dolar.keys()))
    datos = obtener_precio_dolar(tipos_dolar[tipo_dolar])

    if "compra" in datos and "venta" in datos:
        compra, venta = datos["compra"], datos["venta"]
        monto = st.number_input("Ingrese el monto a convertir:", min_value=0.0, format="%.2f")
        conversion = st.radio("Seleccione el tipo de conversión:", ["Pesos a Dólares", "Dólares a Pesos"])

        if st.button("Convertir"):
            if conversion == "Pesos a Dólares":
                resultado = monto / venta
                st.success(f"💵 {monto} ARS equivale a **{resultado:.2f} USD**")
            else:
                resultado = monto * compra
                st.success(f"💵 {monto} USD equivale a **{resultado:.2f} ARS**")
                
def obtener_noticias():
    """Obtiene noticias sobre el dólar en Argentina desde Google News RSS."""
    try:
        feed_url = "https://news.google.com/rss/search?q=dólar+Argentina&hl=es-419&gl=AR&ceid=AR:es"
        feed = feedparser.parse(feed_url)
        noticias = []

        for entry in feed.entries[:10]:
            noticias.append({
                'titulo': entry.title,
                'enlace': entry.link,
                'fecha': entry.published if 'published' in entry else "Fecha no disponible",
                'fuente': entry.source.title if 'source' in entry else "Fuente desconocida"
            })

        return noticias if noticias else [{"titulo": "No hay noticias disponibles", "enlace": "#", "fecha": "", "fuente": ""}]
    except Exception as e:
        return [{"titulo": f"Error al obtener noticias: {e}", "enlace": "#", "fecha": "", "fuente": ""}]

def mostrar_noticias():
    st.title("📰 Novedades y Noticias sobre el Dólar en Argentina")
    if st.button("🔄 Actualizar Noticias"):
        noticias = obtener_noticias()
    else:
        noticias = obtener_noticias()
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    st.write(f"📅 **Última actualización:** {fecha_hoy}")
    
    for noticia in noticias:
        st.write(f"**{noticia['titulo']}**")
        st.write(f"📅 {noticia['fecha']} | 📰 {noticia['fuente']}")
        st.markdown(f"[Ver noticia completa]({noticia['enlace']})")
        st.markdown("---")

# =========================
# 📌 MENÚ PRINCIPAL
# =========================
if __name__ == "__main__":
    st.sidebar.title("📌 Menú")
    menu_seleccionado = st.sidebar.radio("Seleccione una opción:", ["Precios", "Variación de Cotizaciones", "Convertir", "Novedades y Noticias", "Predicción del Dólar Blue"])
    if menu_seleccionado == "Precios":
        mostrar_precios()
    elif menu_seleccionado == "Variación de Cotizaciones":
        mostrar_variacion()
    elif menu_seleccionado == "Convertir":
        convertir_monedas()
    elif menu_seleccionado == "Novedades y Noticias":
        mostrar_noticias()
    elif menu_seleccionado == "Predicción del Dólar Blue":
        mostrar_prediccion()
