import pandas as pd
import openpyxl
import csv
import streamlit as st
import os
import plotly.graph_objects as go
from io import BytesIO
import matplotlib.pyplot as plt
import plotly.express as px




st.set_page_config(page_title="Finanzas de Pepe", page_icon="💸", layout="wide", initial_sidebar_state="expanded")
st.title("Finanzas de Pepe 💸")
st.markdown("🆕 El motivo es llevar un registro puntual de mis finanzas, ver en que gasto y cuales son las metas a futuro.", unsafe_allow_html=True)


sheet_url = "https://docs.google.com/spreadsheets/d/1xDqEMF5egH2QwiKwmO0AH2GUewARWbFJIfFwkh2X45o/export?format=csv"

# Leer los datos
df = pd.read_csv(sheet_url)
  
df["Dia"] = pd.to_datetime(df["Dia"], dayfirst=True, errors='coerce')
mes_actual = df["Dia"].dt.month_name().mode()[0]

# Calcular métricas
total_ingresos = df["Ingreso"].sum()
total_gasto_fijo = df["Gasto fijo"].sum()
total_gasto_variable = df["Gastos variables"].sum()
balance = total_ingresos - total_gasto_fijo - total_gasto_variable

st.subheader(f"📊 Resumen del mes: {mes_actual}")
st.metric("Ingresos", f"${total_ingresos:,.2f}")
st.metric("Gastos Fijos", f"${total_gasto_fijo:,.2f}")
st.metric("Gastos Variables", f"${total_gasto_variable:,.2f}")
st.metric("Balance", f"${balance:,.2f}")




def grafica1():
    # URL del sheet "Resumen"
    url_resumen = "https://docs.google.com/spreadsheets/d/1xDqEMF5egH2QwiKwmO0AH2GUewARWbFJIfFwkh2X45o/export?format=csv&gid=358794166"

    # Leer datos
    Resumen = pd.read_csv(url_resumen)

    # Crear columna auxiliar de tipo (puedes reemplazar luego por valores reales si gustas)
    Resumen["Tipo"] = "Deuda"

    # Calcular total acumulado
    total = Resumen["Monto a pagar"].sum()

    # Crear gráfica
    fig = px.bar(
        Resumen,
        x="Concepto",
        y="Monto a pagar",
        color="Tipo",
        text="Monto a pagar",
        title="Deudas / Gastos largos por concepto",
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Concepto",
        yaxis_title="Monto ($)",
        title_x=0.5,
        height=400,
        barmode="stack"
    )

    return fig, total

figura1, total_deuda = grafica1()




def figura2():
    url_diario = "https://docs.google.com/spreadsheets/d/1xDqEMF5egH2QwiKwmO0AH2GUewARWbFJIfFwkh2X45o/export?format=csv"
    df = pd.read_csv(url_diario)

    # Sumar totales
    total_ingreso = df["Ingreso"].sum()
    total_fijo = df["Gasto fijo"].sum()
    total_variable = df["Gastos variables"].sum()

    # Crear DataFrame resumen
    data = pd.DataFrame({
        "Tipo": ["Ingreso", "Gasto fijo", "Gastos variables"],
        "Monto": [total_ingreso, total_fijo, total_variable]
    })

    # Crear gráfica de barras
    fig = px.bar(
        data,
        x="Tipo",
        y="Monto",
        color="Tipo",
        text="Monto",
        title="Comparativa general: Ingresos vs Gastos",
    )

    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(
        yaxis_title="Monto ($)",
        xaxis_title="",
        title_x=0.5,
        showlegend=False,
        height=400
    )

    return fig




def figura3():
    url_diario = "https://docs.google.com/spreadsheets/d/1xDqEMF5egH2QwiKwmO0AH2GUewARWbFJIfFwkh2X45o/export?format=csv"
    df = pd.read_csv(url_diario)

    # Convertir fecha
    df["Dia"] = pd.to_datetime(df["Dia"], dayfirst=True, errors="coerce")

    # Calcular gasto total por fila
    df["Gasto total"] = df["Gasto fijo"].fillna(0) + df["Gastos variables"].fillna(0)

    # Agrupar ingresos y gasto total por día
    balance = df.groupby("Dia")[["Ingreso", "Gasto total"]].sum().reset_index()
    balance["Balance"] = balance["Ingreso"] - balance["Gasto total"]

    # Gráfica de líneas con ingreso, gasto total y balance
    fig = px.line(
        balance,
        x="Dia",
        y=["Ingreso", "Gasto total", "Balance"],
        title="Balance diario: ingresos vs gastos",
        markers=True,
        labels={"value": "Monto ($)", "variable": "Concepto"},
    )

    fig.update_layout(title_x=0.5)
    return fig

def figura4():
    # Leer tus datos de Google Sheets
    url = "https://docs.google.com/spreadsheets/d/1xDqEMF5egH2QwiKwmO0AH2GUewARWbFJIfFwkh2X45o/export?format=csv"
    df = pd.read_csv(url)

    # Calcular el total
    total_gasto_fijo = df["Gasto fijo"].sum()

    # Crear una sola barra con el total
    fig = px.bar(
        x=["Gastos fijos"], 
        y=[total_gasto_fijo],
        text=[f"${total_gasto_fijo:,.2f}"],
        title="Gastos Fijos por Mes",
        labels={"x": "", "y": "Monto ($)"}
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(title_x=0.5, showlegend=False, height=300)

    return fig



figura2 = figura2()
figura3 = figura3()
figura4 = figura4()


# Crear columnas
c1, c2, c3 = st.columns([4, 3, 4])

# Columna 1: tu gráfica de cuentas por pagar
with c1:
    st.plotly_chart(figura1, use_container_width=True)
    st.markdown(f"💰 **Total acumulado:** ${total_deuda:,.2f}")

with c2:
    st.plotly_chart(figura2, use_container_width=True)
with c3:
    st.plotly_chart(figura3, use_container_width=True)


c4, c5, c6 = st.columns([4, 3, 4])
with c4:
    st.plotly_chart(figura4, use_container_width=True)

