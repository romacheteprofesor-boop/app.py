import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Cotizador Maestro de Cancelería", layout="wide")

# Inicializar la lista de ventanas en la sesión para que no se borre al recargar
if "lista_ventanas" not in st.session_state:
    st.session_state.lista_ventanas = []
if "precio_agarradera" not in st.session_state:
    st.session_state.precio_agarradera = 0.0

st.title("🪟 Cotizador Maestro de Cancelería")
st.markdown("---")

# --- 1. CONFIGURACIÓN DE PRECIOS (BARRA LATERAL) ---
st.sidebar.header("⚙️ Precios Base (Tramo 6m)")

p_riel = st.sidebar.number_input("Riel", value=323.84)
p_traslape = st.sidebar.number_input("Traslape", value=466.18)
p_cerco = st.sidebar.number_input("Cerco", value=395.57)
p_zoclo = st.sidebar.number_input("Zoclo Puerta", value=629.67)
p_cabezal = st.sidebar.number_input("Cabezal", value=316.96)
p_jamba = st.sidebar.number_input("Jamba", value=461.16)
p_vidrio = st.sidebar.number_input("Vidrio (m²)", value=277.00)

# Precios por metro lineal
pm = {
    "riel": p_riel / 6,
    "traslape": p_traslape / 6,
    "cerco": p_cerco / 6,
    "zoclo_puerta": p_zoclo / 6,
    "cabezal": p_cabezal / 6,
    "jamba": p_jamba / 6,
    "vidrio": p_vidrio
}

# --- 2. ENTRADA DE DATOS ---
col_form, col_res = st.columns([1, 2])

with col_form:
    st.subheader("📝 Nueva Ventana")
    with st.form("form_vta", clear_on_submit=True):
        ancho = st.number_input("Ancho (m)", min_value=0.0, step=0.01, value=1.0)
        alto = st.number_input("Alto (m)", min_value=0.0, step=0.01, value=1.0)
        cant = st.number_input("Cantidad de piezas", min_value=1, step=1, value=1)
        agarr = st.number_input("Agarraderas por ventana", min_value=0, step=1, value=1)
        
        if st.form_submit_button("Añadir a la lista"):
            st.session_state.lista_ventanas.append({
                "Ancho": ancho, "Alto": alto, "Cant": cant, "Agarr": agarr
            })
            st.rerun()

    if any(v['Agarr'] > 0 for v in st.session_state.lista_ventanas):
        st.session_state.precio_agarradera = st.number_input("Precio unitario Agarradera ($)", value=st.session_state.precio_agarradera)

    if st.button("🗑️ Borrar Lista"):
        st.session_state.lista_ventanas = []
        st.rerun()

# --- 3. CÁLCULOS Y TICKET ---
with col_res:
    st.subheader("📊 Resumen de Cotización")
    
    if st.session_state.lista_ventanas:
        # Tabla de medidas
        df = pd.DataFrame(st.session_state.lista_ventanas)
        st.dataframe(df, use_container_width=True)

        porc_mo = st.slider("Porcentaje de Mano de Obra (%)", 0, 100, 35)

        # Lógica de consumo (Tu fórmula exacta)
        m_riel = sum(v["Ancho"] * v["Cant"] for v in st.session_state.lista_ventanas)
        m_cabezal = sum(v["Ancho"] * v["Cant"] for v in st.session_state.lista_ventanas)
        m_jamba = sum((v["Alto"] * 3) * v["Cant"] for v in st.session_state.lista_ventanas)
        m_traslape = sum((v["Alto"] * 2) * v["Cant"] for v in st.session_state.lista_ventanas)
        m_cerco = sum((v["Alto"] * 2) * v["Cant"] for v in st.session_state.lista_ventanas)
        m_zoclo = sum((v["Ancho"] * 1) * v["Cant"] for v in st.session_state.lista_ventanas)
        m2_vidrio = sum((v["Ancho"] * v["Alto"]) * v["Cant"] for v in st.session_state.lista_ventanas)
        total_agarr = sum(v["Agarr"] * v["Cant"] for v in st.session_state.lista_ventanas)

        # Cálculos de dinero
        costo_aluminio = (m_riel * pm["riel"]) + (m_cabezal * pm["cabezal"]) + \
                         (m_jamba * pm["jamba"]) + (m_traslape * pm["traslape"]) + \
                         (m_cerco * pm["cerco"]) + (m_zoclo * pm["zoclo_puerta"])
        
        costo_vidrio = m2_vidrio * pm["vidrio"]
        costo_mat_base = costo_aluminio + costo_vidrio
        costo_extras = costo_mat_base * 0.20
        costo_herrajes = total_agarr * st.session_state.precio_agarradera
        
        monto_con_iva = costo_mat_base + costo_extras + costo_herrajes
        iva_materiales = monto_con_iva * 0.16
        mano_obra = monto_con_iva * (porc_mo / 100)
        total_final = monto_con_iva + iva_materiales + mano_obra

        # TICKET VISUAL
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Materiales Base:** ${costo_mat_base:,.2f}")
            st.write(f"**Extras (20%):** ${costo_extras:,.2f}")
            st.write(f"**Agarraderas:** ${costo_herrajes:,.2f}")
        with c2:
            st.write(f"**IVA Materiales (16%):** ${iva_materiales:,.2f}")
            st.write(f"**Mano de Obra ({porc_mo}%):** ${mano_obra:,.2f}")
        
        st.info(f"### TOTAL NETO: ${total_final:,.2f}")
        
    else:
        st.info("Agregue ventanas para ver el cálculo.")