import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import re

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="HN MIP-IA: Explorador de Honduras", page_icon="🇭🇳", layout="wide"
)

# ==========================================
# 2. CARGA Y VALIDACIÓN RIGUROSA DE LA MATRIZ DB
# ==========================================
ruta_csv = "data/mip_honduras_2013.csv"

@st.cache_data
def cargar_datos(ruta):
    """Carga la matriz de coeficientes técnicos desde el CSV,
    estableciendo la primera columna como índice.
    """
    df = pd.read_csv(ruta, index_col=0)
    return df

# Manejo de excepciones en caso de que el archivo no exista
try:
    matriz_db = cargar_datos(ruta_csv)
except FileNotFoundError:
    st.error(
        f"❌ **Error crítico:** No se encontró el archivo en la ruta `{ruta_csv}`."
        " Asegúrate de haber ejecutado el script de exportación en Google Colab"
        " y de que la carpeta 'data' esté en el repositorio."
    )
    st.stop()

# Comprobación estricta de dimensiones (95x95)
filas, columnas = matriz_db.shape
if filas != 95 or columnas != 95:
    st.error(
        f"❌ **Error de dimensiones:** Se esperaban 95x95, pero el archivo tiene"
        f" dimensiones {filas}x{columnas}."
    )
    st.stop()

# Comprobación estricta de que los 9,025 coeficientes sean numéricos y finitos
matriz_numerica = matriz_db.apply(pd.to_numeric, errors="coerce")
valores_nulos = matriz_numerica.isna().sum().sum()
valores_no_finitos = np.isinf(matriz_numerica.to_numpy()).sum()

if valores_nulos > 0 or valores_no_finitos > 0:
    st.error(
        "❌ **Error de datos:** La matriz contiene valores no numéricos,"
        f" faltantes ({valores_nulos}) o infinitas ({valores_no_finitos})."
    )
    st.stop()

# Garantizar compatibilidad estricta de nombres y orden entre filas y columnas
if not matriz_numerica.index.equals(matriz_numerica.columns):
    st.error(
        "❌ **Error de integridad:** Los nombres o el orden de las filas (actividades proveedoras)"
        " y las columnas (actividades compradoras) no son consistentes."
    )
    st.stop()

# Garantizar que los cálculos posteriores utilicen la matriz validada
matriz_db = matriz_numerica

# Función para sanitizar nombres de archivos
def limpiar_nombre_archivo(nombre):
    sub_limpio = re.sub(r'[^a-zA-Z0-9_]', '_', nombre)
    return re.sub(r'_+', '_', sub_limpio).strip('_').lower()

# ==========================================
# 3. INTERFAZ DE USUARIO (UI) - TÍTULO Y FUENTE
# ==========================================
st.title("HN MIP-IA: Explorador Intersectorial Ampliado de Honduras")
st.markdown(
    "**Fuente oficial de datos:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013, "
    "**Tabla 12 (DB)** (Matriz de coeficientes técnicos aplicada sobre la producción bruta total)."
)
st.markdown("---")

# Crear las dos pestañas principales del proyecto
tab1, tab2 = st.tabs(["📊 Proveedores directos", "👥 Clientes directos"])

# ==========================================
# 4. PESTAÑA 1: PROVEEDORES DIRECTOS (Eje de Columnas)
# ==========================================
with tab1:
    st.header("🔍 Análisis de Insumos / Proveedores")
    st.markdown(
        "Este módulo analiza la **estructura de requerimientos intermedios directos** de una actividad económica compradora. "
        "Permite identificar de qué sectores proviene directamente su gasto intermedio por cada lempira producido."
    )

    lista_actividades = list(matriz_db.columns)
    actividad_compradora = st.selectbox(
        "Seleccione una actividad económica (industria compradora):",
        lista_actividades,
        key="sb_proveedores"
    )

    # Cálculos para Proveedores (Operaciones en Columnas)
    coef_proveedores = matriz_db[actividad_compradora]
    prov_activos = coef_proveedores[coef_proveedores > 0]
    prov_ordenados = prov_activos.sort_values(ascending=False)
    top_10_prov = prov_ordenados.head(10)

    # Sumas de la columna
    suma_total_prov = coef_proveedores.sum()
    centavos_prov = suma_total_prov * 100

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Top 10: Proveedores directos")
        df_top10_prov = pd.DataFrame({
            "Sector Proveedor": top_10_prov.index,
            "Coeficiente Técnico (a_ij)": top_10_prov.values
        })
        df_top10_prov.index = range(1, len(df_top10_prov) + 1)
        
        # Mostrar con formato estilizado a 6 decimales
        st.dataframe(
            df_top10_prov.style.format({"Coeficiente Técnico (a_ij)": "{:.6f}"}),
            width="stretch"
        )

        # Botón para descargar resultados completos en CSV con nombre seguro
        df_completo_prov = pd.DataFrame({
            "Sector Proveedor": prov_ordenados.index,
            "Coeficiente Técnico (a_ij)": prov_ordenados.values
        })
        csv_prov = df_completo_prov.to_csv(index=False, encoding="utf-8-sig")
        nombre_prov_limpio = limpiar_nombre_archivo(actividad_compradora)
        st.download_button(
            label="📥 Descargar lista de proveedores (CSV)",
            data=csv_prov,
            file_name=f"prov_{nombre_prov_limpio}.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("📉 Representación Gráfica")
        # Preparar datos para el gráfico de Altair
        chart_data_prov = pd.DataFrame({
            "Sector": top_10_prov.index,
            "Coeficiente Técnico": top_10_prov.values
        })
        
        # Gráfico horizontal interactivo con orden descendente exacto, límites de etiqueta y tooltips completos
        grafico_prov = alt.Chart(chart_data_prov).mark_bar().encode(
            x=alt.X('Coeficiente Técnico:Q', title='Coeficiente Técnico (a_ij)'),
            y=alt.Y('Sector:N', sort='-x', title='Sector Proveedor', 
                    axis=alt.Axis(labelLimit=250)),
            tooltip=[alt.Tooltip('Sector:N', title='Sector Proveedor'), 
                     alt.Tooltip('Coeficiente Técnico:Q', format='.6f', title='Coeficiente (a_ij)')]
        ).properties(height=350).interactive()
        
        st.altair_chart(grafico_prov, width="stretch")

    st.markdown("---")
    st.subheader("💡 Resumen de Requerimientos Intermedios Compradores")

    m1, m2 = st.columns(2)
    with m1:
        st.metric(
            label="Suma de Coeficientes Técnicos de la Columna",
            value=f"{suma_total_prov:.6f}",
        )
    with m2:
        st.metric(
            label="Insumos Intermedios Directos",
            value=f"{centavos_prov:.2f} centavos por L 1.00 de producción",
        )

    st.info(
        "📝 **Nota metodológica importante (Proveedores):** Los valores mostrados corresponden a "
        "los coeficientes técnicos directos de la **Tabla 12 (DB)** publicada por el BCH. "
        "Estos coeficientes reflejan exclusivamente los **requerimientos directos** de insumos intermedios "
        "necesarios para generar un lempira de producción en el sector seleccionado, "
        "**y no constituyen multiplicadores de Leontief** (los cuales capturan efectos directos e indirectos)."
    )

# ==========================================
# 5. PESTAÑA 2: CLIENTES DIRECTOS (Eje de Filas)
# ==========================================
with tab2:
    st.header("🔍 Análisis de Destinos / Clientes")
    st.markdown(
        "Este módulo analiza la importancia de una actividad económica proveedora como suministradora de insumos directos. "
        "Permite identificar las actividades compradoras que utilizan con mayor intensidad su producción."
    )

    actividad_proveedora = st.selectbox(
        "Seleccione una actividad económica (industria proveedora):",
        lista_actividades,
        key="sb_clientes"
    )

    # Cálculos para Clientes (Operaciones en Filas de la Matriz A = [a_ij])
    coef_clientes = matriz_db.loc[actividad_proveedora]
    clie_activos = coef_clientes[coef_clientes > 0]
    clie_ordenados = clie_activos.sort_values(ascending=False)
    top_10_clie = clie_ordenados.head(10)

    col3, col4 = st.columns([1, 1])

    with col3:
        st.subheader("Top 10: Actividades usuarias directas")
        df_top10_clie = pd.DataFrame({
            "Sector Cliente (Comprador)": top_10_clie.index,
            "Coeficiente Técnico (a_ij)": top_10_clie.values
        })
        df_top10_clie.index = range(1, len(df_top10_clie) + 1)
        
        # Mostrar con formato estilizado a 6 decimales
        st.dataframe(
            df_top10_clie.style.format({"Coeficiente Técnico (a_ij)": "{:.6f}"}),
            width="stretch"
        )

        # Botón para descargar resultados completos en CSV con nombre seguro
        df_completo_clie = pd.DataFrame({
            "Sector Cliente (Comprador)": clie_ordenados.index,
            "Coeficiente Técnico (a_ij)": clie_ordenados.values
        })
        csv_clie = df_completo_clie.to_csv(index=False, encoding="utf-8-sig")
        nombre_clie_limpio = limpiar_nombre_archivo(actividad_proveedora)
        st.download_button(
            label="📥 Descargar lista de clientes (CSV)",
            data=csv_clie,
            file_name=f"clie_{nombre_clie_limpio}.csv",
            mime="text/csv"
        )

    with col4:
        st.subheader("📉 Representación Gráfica")
        # Preparar datos para el gráfico de Altair
        chart_data_clie = pd.DataFrame({
            "Sector": top_10_clie.index,
            "Coeficiente Técnico": top_10_clie.values
        })
        
        # Gráfico horizontal interactivo con orden descendente exacto, límites de etiqueta y tooltips completos
        grafico_clie = alt.Chart(chart_data_clie).mark_bar().encode(
            x=alt.X('Coeficiente Técnico:Q', title='Coeficiente Técnico (a_ij)'),
            y=alt.Y('Sector:N', sort='-x', title='Sector Cliente (Comprador)', 
                    axis=alt.Axis(labelLimit=250)),
            tooltip=[alt.Tooltip('Sector:N', title='Sector Cliente'), 
                     alt.Tooltip('Coeficiente Técnico:Q', format='.6f', title='Coeficiente (a_ij)')]
        ).properties(height=350).interactive()
        
        st.altair_chart(grafico_clie, width="stretch")

    st.markdown("---")
    st.subheader("💡 Contexto y Advertencia Metodológica (Clientes)")

    st.warning(
        "⚠️ **Interpretación económica fundamental del análisis por fila:**\n\n"
        "1. **¿Qué representan estos coeficientes?** Indican la intensidad con la que cada actividad "
        "compradora utiliza como insumo directo el producto de la actividad proveedora seleccionada por cada lempira "
        "que dicha actividad compradora produce.\n\n"
        "2. **¿Qué NO representan?**\n"
        "   * **No representan participaciones de mercado / ventas:** Los coeficientes técnicos no muestran el porcentaje de ventas de la industria "
        "proveedora destinadas a cada sector. No indica qué proporción del mercado capta cada comprador.\n"
        "   * **No sumabilidad:** Sumar verticalmente estos coeficientes no tiene un significado económico directo "
        "relacionado con la producción agregada o las ventas totales del sector proveedor. Evite la acumulación de coeficientes por fila.\n"
        "   * **No constituyen multiplicadores:** Tampoco capturan los efectos inducidos o indirectos del modelo de Leontief."
    )
