import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="BI Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("ventas.csv")
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

df = load_data()

st.sidebar.header("Filtros")
region = st.sidebar.multiselect("Región", df["region"].unique(), df["region"].unique())
producto = st.sidebar.multiselect("Producto", df["producto"].unique(), df["producto"].unique())

df_filtered = df[(df["region"].isin(region)) & (df["producto"].isin(producto))]

ventas_totales = df_filtered["ventas"].sum()
ventas_promedio = df_filtered["ventas"].mean()

col1, col2 = st.columns(2)
col1.metric("Ventas Totales", f"${ventas_totales:,.0f}")
col2.metric("Promedio Ventas", f"${ventas_promedio:,.0f}")

st.markdown("---")

st.subheader("Tendencia de Ventas")
ventas_tiempo = df_filtered.groupby("fecha")["ventas"].sum()
fig1, ax1 = plt.subplots()
ventas_tiempo.plot(ax=ax1)
st.pyplot(fig1)

st.subheader("Ventas por Región")
fig2, ax2 = plt.subplots()
sns.barplot(x=df_filtered.groupby("region")["ventas"].sum().index,
            y=df_filtered.groupby("region")["ventas"].sum().values,
            ax=ax2)
st.pyplot(fig2)

st.subheader("Top Productos")
top_prod = df_filtered.groupby("producto")["ventas"].sum().sort_values(ascending=False)
fig3, ax3 = plt.subplots()
top_prod.plot(kind="barh", ax=ax3)
st.pyplot(fig3)

st.subheader("Datos")
st.dataframe(df_filtered)
