import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import re
from google import genai
from google.genai import types

st.markdown("""
<style>
div.st-key-gemini_proveedores button {
    background-color: #5B3294 !important;
    color: white !important;
    font-weight: 400 !important;
    font-size: 18px !important;
    border: 2px solid #8254BA !important;
}

div.st-key-gemini_proveedores button p {
    font-size: 18px !important;
    font-weight: 400 !important;
}

div.st-key-gemini_proveedores button:hover {
    background-color: #7446AD !important;
    border-color: #A784D4 !important;
}

/* Tamaño de las pestañas Proveedores y Clientes */
div[data-baseweb="tab-list"] button[data-baseweb="tab"],
div[data-baseweb="tab-list"] button[data-baseweb="tab"] * {
    font-size: 23px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.st-key-gemini_clientes button[kind="primary"] {
    background: #63369C !important;
    background-color: #63369C !important;
    border: 1px solid #9164C5 !important;
    color: #FFFFFF !important;
    font-weight: 400 !important;
    font-size: 17px !important;
}

.st-key-gemini_clientes button[kind="primary"] p {
    color: #FFFFFF !important;
    font-weight: 400 !important;
    font-size: 17px !important;
}

.st-key-gemini_clientes button[kind="primary"]:hover {
    background: #8052B5 !important;
    background-color: #8052B5 !important;
}
</style>
""", unsafe_allow_html=True)

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
# INTERPRETACIÓN CON IA (SIN CÁLCULOS EXTERNOS)
# ==========================================
MODELO_GEMINI = "gemini-3.6-flash"  # Modelo verificado en Colab; sujeto a disponibilidad de API


INSTRUCCIONES_GEMINI = """
Eres un economista especializado en la estructura productiva de Honduras.
Tu función es explicar de manera atractiva, clara y rigurosa las relaciones
intersectoriales que muestran los resultados de la Matriz Insumo-Producto
de Honduras de 2013, publicada por el Banco Central de Honduras.

ESTILO:
- Escribe como un analista económico que explica sus hallazgos a un lector interesado.
- Comienza con una idea económica relevante sobre la actividad seleccionada.
- Utiliza un lenguaje natural, fluido y accesible, sin perder precisión técnica.
- Evita respuestas mecánicas, enumeraciones extensas y lenguaje excesivamente académico.
- Redacta tres párrafos breves, sin subtítulos.

CONTENIDO:
- Primer párrafo: presenta la actividad y explica sus relaciones de compra
  o suministro con otras actividades económicas.
- Segundo párrafo: destaca únicamente los tres coeficientes técnicos
  directos más altos y explica qué revela su composición sectorial.
- Tercer párrafo: presenta una síntesis económica de los resultados.
  En PROVEEDORES, incluye la suma de la columna completa y su
  equivalencia en centavos por lempira de producción.
  En CLIENTES, no calcules ni presentes sumas de filas.

RIGOR:
- Utiliza exclusivamente los resultados numéricos proporcionados por Python.
- No inventes cifras, relaciones, características sectoriales ni fuentes.
- No atribuyas importancia económica nacional, causalidad o impactos
  que no puedan establecerse a partir de los datos suministrados.
- En PROVEEDORES, a_ij expresa insumos del proveedor i por lempira
  de producción del comprador j.
- En CLIENTES, a_ij expresa insumos del proveedor i por lempira
  de producción de cada comprador j; no representa ventas totales
  ni participación de mercado.
- Los coeficientes son directos, no multiplicadores de Leontief.
- Menciona brevemente que los datos corresponden a 2013.
- No dediques párrafos a explicar limitaciones metodológicas.
  Si es necesario, incorpora una sola precisión al final.
"""



def interpretar_con_gemini(tipo, actividad, resultados, suma_columna=None):
    """Solicita una explicación; los datos y cálculos provienen exclusivamente de Python."""
    try:
        clave_api = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        clave_api = None
      
    
    if not clave_api:
        st.warning("Gemini no está configurado. Añadí GEMINI_API_KEY a los secretos de Streamlit.")
        return

    detalle = "\n".join(
        f"- {sector}: {float(coef):.6f}"
        for sector, coef in resultados.items()
    )
    contexto = (
        f"Módulo: {tipo}\nActividad seleccionada: {actividad}\n"
        f"Los diez coeficientes técnicos directos más altos (orden descendente):\n{detalle}"
    )
    if tipo == "PROVEEDORES" and suma_columna is not None:
        contexto += f"\nSuma de coeficientes de la columna completa: {suma_columna:.6f}"

    try:
        cliente = genai.Client(api_key=clave_api)
        respuesta = cliente.models.generate_content(
            model=MODELO_GEMINI,
            contents=contexto + "\nExplica la lectura económica de estos resultados.",
            config=types.GenerateContentConfig(
                system_instruction=INSTRUCCIONES_GEMINI,
                temperature=0.2,
                max_output_tokens=2048,
            ),
        )
        if respuesta.text:
            st.markdown(respuesta.text)
            st.caption("Interpretación generada por IA; verificá sus afirmaciones con las tablas y notas metodológicas.")
        else:
            st.warning("Gemini no devolvió una interpretación. Intentá nuevamente.")
    except Exception as error:
        codigo = getattr(error, "code", None)
        if codigo == 429:
            st.warning("Gemini alcanzó su límite de solicitudes o cuota. Intentá más tarde.")
        elif codigo in (401, 403):
            st.error("No fue posible autenticar la API de Gemini. Revisá la clave y sus permisos en Streamlit.")
        elif codigo == 404:
            st.error("El modelo configurado no está disponible para esta API. Revisá MODELO_GEMINI.")
        else:
            st.error(f"No fue posible obtener la interpretación de Gemini ({type(error).__name__}).")

        st.error(f"Diagnóstico HTTP: {codigo}")
        st.error(f"Detalle técnico: {str(error)[:500]}")


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
            y=alt.Y('Sector:N', sort='-x', title=None,
        axis=alt.Axis(
            title=None,
            labelLimit=350,
            labelFontSize=12
        )),
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

    st.subheader("🤖 Interpretación asistida por Gemini")
    st.caption("La IA interpreta los coeficientes calculados por Python; no realiza cálculos adicionales.")
    if st.button("✨ Generar análisis económico con IA", type="primary", use_container_width=True, key="gemini_proveedores"):
        with st.spinner("Gemini está interpretando los resultados..."):
            interpretar_con_gemini(
                "PROVEEDORES", actividad_compradora, top_10_prov,
                suma_columna=suma_total_prov,
            )

    with st.expander("📘 Nota metodológica importante (Proveedores)"):
        st.markdown(
            """
            <div style="color:#2997FF; font-size:16px; line-height:1.7;">
            Los valores mostrados corresponden a los coeficientes técnicos
            directos de la <b>Tabla 12 (DB)</b> publicada por el BCH.
            Estos coeficientes reflejan exclusivamente los
            <b>requerimientos directos</b> de insumos intermedios
            necesarios para generar un lempira de producción en el
            sector seleccionado, <b>y no constituyen multiplicadores
            de Leontief</b> (los cuales capturan efectos directos
            e indirectos).
            </div>
            """,
            unsafe_allow_html=True
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
               y=alt.Y(
        'Sector:N',
        sort='-x',
        title=None,
        axis=alt.Axis(
            title=None,
            labelLimit=350,
            labelFontSize=12
        )
    ),
            tooltip=[alt.Tooltip('Sector:N', title='Sector Cliente'), 
                     alt.Tooltip('Coeficiente Técnico:Q', format='.6f', title='Coeficiente (a_ij)')]
        ).properties(height=350).interactive()
        
        st.altair_chart(grafico_clie, width="stretch")
    

    st.subheader("🤖 Interpretación asistida por Gemini")

    st.caption(
        "La IA interpreta los coeficientes calculados por Python; "
        "no realiza cálculos adicionales."
    )
    
    
    if st.button(
        "✨ Generar análisis económico con IA",
        type="primary",
        use_container_width=True,
        key="gemini_clientes"
    ):
        with st.spinner("Gemini está interpretando los resultados..."):
            interpretar_con_gemini(
                "CLIENTES",
                actividad_proveedora,
                top_10_clie
        )

    with st.expander("📘 Notas metodológicas del análisis de Clientes"):
        st.markdown(
            """
            <div style="color:#C9B879; font-size:16px; line-height:1.7;">

            <b>Interpretación económica fundamental del análisis por fila</b>

            <p><b>1. ¿Qué representan estos coeficientes?</b></p>

            <p>
            Indican la intensidad con la que cada actividad compradora
            utiliza como insumo directo el producto de la actividad
            proveedora seleccionada, por cada lempira que dicha
            actividad compradora produce.
            </p>

            <p><b>2. ¿Qué NO representan?</b></p>

            <p>
            <b>Participaciones de mercado o ventas:</b>
            Los coeficientes técnicos no muestran el porcentaje
            de ventas de la industria proveedora destinadas a
            cada sector. Tampoco indican qué proporción del
            mercado capta cada comprador.
            </p>

            <p>
            <b>Sumabilidad:</b>
            Sumar los coeficientes de una fila no permite
            determinar la producción agregada ni las ventas
            totales del sector proveedor. Por tanto, no debe
            interpretarse esa suma como un indicador económico
            de participación o demanda total.
            </p>

            <p>
            <b>Multiplicadores:</b>
            Estos coeficientes no constituyen multiplicadores
            de Leontief ni capturan los efectos indirectos
            o inducidos sobre el resto de la economía.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )
   
