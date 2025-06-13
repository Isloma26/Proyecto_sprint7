import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Análisis de Autos", layout="wide")

# Título del dashboard
st.title("📊 Dashboard de Anuncios de Venta de Autos")

# Cargar Dataset
car_data = pd.read_csv(
    "vehicles_us.csv")  # leer los datos

# rellenar valores nulos en columnas is_4wd
car_data["is_4wd"] = car_data["is_4wd"].fillna("not 4wd")

# convertor formato de columna date_posted a formato fecha
car_data["date_posted"] = pd.to_datetime(
    car_data["date_posted"], format="%Y-%m-%d")

# Rellenar valores en columna model_year con 0 donde sea NaN y reemplazar 0 por "unknown"
car_data["model_year"] = car_data["model_year"].fillna(
    0).astype(int).replace(0, "unknown")

# Reemplazar 1.0 en la columna is_4wd por "4wd"
car_data["is_4wd"] = car_data["is_4wd"].replace(1.0, "4wd")

# Crear una nueva columna "brand" extrayendo la marca del modelo.
car_data["brand"] = car_data["model"].str.split().str[0]

# Reordenar las columnas por orden alfabetico.
car_data = car_data[sorted(car_data.columns)]

# Condition de los vehículos por marca.
brand_df = car_data.groupby("brand")["condition"].value_counts()

# Precio de los vehículos por marca.
price_df = car_data.groupby("brand")["price"].mean().reset_index()

# Precio de los vehiculos por marca y condición.
odometer_cars = (
    car_data.groupby(["condition", "brand", "price", "odometer"])
    .size()
    .reset_index(name="count")
)


# Histograma
if st.checkbox("Mostrar histograma del kilometraje"):
    st.write("Histograma de kilometraje de los vehículos")
    fig_hist = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig_hist, use_container_width=True)

# Gráfico de dispersión
if st.checkbox("Mostrar gráfico de dispersión (precio vs. kilometraje)"):
    st.write("Relación entre precio y kilometraje")
    fig_scatter = px.scatter(car_data, x="odometer", y="price", color="brand",
                             title="Dispersión Precio vs. Kilometraje", opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)
