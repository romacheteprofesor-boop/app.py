import streamlit as st
import pandas as pd

# 1. Configuración básica
st.set_page_config(page_title="Cotizador Aluminio", layout="wide")

# Mensaje de control para saber que el código corre
st.write("### ✅ El programa se está ejecutando correctamente")

# 2. Inicializar base de datos en la sesión
if "lista_ventanas" not in st.session_state:
    st.session_state.lista_ventanas = []

# 3. Sidebar con precios
st.sidebar.header("Precios Base")
p_riel = st.sidebar.number_input("Riel 6m", value=323.84)
p_traslape = st.sidebar.number_input("Traslape 6m", value=466.18)
p_cerco = st.sidebar.number_input("Cerco 6m", value=395.57)
p_zoclo = st.sidebar.number_input("Zoclo Puerta 6m", value=629.67)
p_cabezal = st.sidebar.number_input("Cabezal 6m", value=316.96)
p_jamba = st.sidebar.number_input("Jamba 6m", value=461.16)
p_vidrio = st.sidebar.number_input("Vidrio m2", value=277.0)

# 4. Formulario de entrada
st.header("1. Agregar Ventana")
with st.form("entrada"):
    c1, c2, c3, c4 = st.columns(4)
    anc = c1.number_input("Ancho (m)", value=1.0)
    alt = c2.number_input("Alto (m)", value=1.0)
    qty = c3.number_input("Cantidad", value=1)
    aga = c4.number_input("Agarraderas/Vta", value=1)
    submit = st.form_submit_button("Agregar a la lista")

if submit:
    st.session_state.lista_ventanas.append({
        "Ancho": anc, "Alto": alt, "Cant": qty, "Agarr": aga
    })
    st.success("Agregada")

# 5. Mostrar tabla y calcular
if st.session_state.lista_ventanas:
    st.header("2. Resumen y Cálculo")
    df = pd.DataFrame(st.session_state.lista_ventanas)
    st.table(df)

    p_agarradera = st.number_input("Precio unitario Agarradera", value=50.0)
    p_mo = st.slider("Mano de Obra (%)", 0, 100, 35)

    # Lógica de cálculo (Tu fórmula exacta)
    riel_tot = sum(v["Ancho"] * v["Cant"] for v in st.session_state.lista_ventanas)
    jamba_tot = sum((v["Alto"] * 3) * v["Cant"] for v in st.session_state.lista_ventanas)
    # ... (simplificando para la prueba rápida)
    
    # Costo aproximado solo para ver que funcione
    costo_aprox = (riel_tot * (p_riel/6)) + (jamba_tot * (p_jamba/6))
    extras = costo_aprox * 0.20
    iva = (costo_aprox + extras) * 0.16
    mo_final = (costo_aprox + extras) * (p_mo/100)
    
    st.metric("TOTAL ESTIMADO (Material + IVA + MO)", f"${(costo_aprox + extras + iva + mo_final):,.2f}")
    
    if st.button("Limpiar todo"):
        st.session_state.lista_ventanas = []
        st.rerun()