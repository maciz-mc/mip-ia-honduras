import numpy as np
import pandas as pd
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="MIP-IA: Explorador de Honduras", page_icon="🇭🇳", layout="wide"
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
      f" faltantes ({valores_nulos}) o infinitos ({valores_no_finitos})."
  )
  st.stop()

# Garantizar que los cálculos posteriores utilicen la matriz validada
matriz_db = matriz_numerica


# ==========================================
# 3. INTERFAZ DE USUARIO (UI) CON STREAMLIT
# ==========================================

# Título y Fuente oficiales
st.title("🇭🇳 MIP-IA: Explorador de relaciones intersectoriales de Honduras")
st.markdown(
    "**Fuente:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013,"
    " **Tabla 12 (DB)** (Matriz de coeficientes técnicos aplicada sobre"
    " producción bruta total)."
)
st.markdown("---")

# Lista desplegable utilizando las columnas (industrias compradoras)
# Resuelve las discrepancias menores de denominación en filas (12, 86 y 87)
lista_actividades = list(matriz_db.columns)
actividad_seleccionada = st.selectbox(
    "🔍 Seleccione una actividad económica (industria compradora):",
    lista_actividades,
)

# ==========================================
# 4. PROCESAMIENTO Y CÁLCULOS ECONÓMICOS
# ==========================================

# Extraer la columna correspondiente a la actividad seleccionada
coeficientes_actividad = matriz_db[actividad_seleccionada]

# Filtrar proveedores con coeficientes estrictamente mayores a cero
proveedores_activos = coeficientes_actividad[coeficientes_actividad > 0]

# Ordenar los proveedores de mayor a menor coeficiente técnico
proveedores_ordenados = proveedores_activos.sort_values(ascending=False)

# Seleccionar los 10 principales requerimientos directos
top_10 = proveedores_ordenados.head(10)

# Calcular la suma total de los 95 coeficientes técnicos de la actividad
suma_total_coeficientes = coeficientes_actividad.sum()
centavos_por_lempira = suma_total_coeficientes * 100

# ==========================================
# 5. VISUALIZACIÓN DE RESULTADOS
# ==========================================

col1, col2 = st.columns([1, 1])

with col1:
  st.subheader("📊 Diez principales requerimientos intermedios directos")
  st.markdown(
      f"Principales insumos requeridos por **{actividad_seleccionada}**:"
  )

  # Preparar tabla formateada para visualización
  df_top10 = pd.DataFrame({
      "Sector Proveedor": top_10.index,
      "Coeficiente Técnico (a_ij)": top_10.values,
  })
  df_top10.index = range(1, len(df_top10) + 1)
  st.dataframe(df_top10, use_container_width=True)

with col2:
  st.subheader("📉 Representación Gráfica")
  # Gráfico de barras horizontal nativo de Streamlit
  st.bar_chart(top_10, horizontal=True)

st.markdown("---")

# ==========================================
# 6. MÉTRICAS DE RESUMEN Y NOTA METODOLÓGICA
# ==========================================

st.subheader("💡 Resumen de Requerimientos Intermedios")

m1, m2 = st.columns(2)
with m1:
  st.metric(
      label="Suma de Coeficientes Técnicos",
      value=f"{suma_total_coeficientes:.6f}",
  )
with m2:
  st.metric(
      label="Insumos Intermedios Directos",
      value=f"{centavos_por_lempira:.2f} centavos por L 1.00 de producción",
  )

# Nota metodológica obligatoria
st.info(
    "📝 **Nota metodológica importante:** Los valores mostrados corresponden a"
    " los coeficientes técnicos directos de la **Tabla 12 (DB)** publicada por"
    " el BCH. Estos coeficientes reflejan exclusivamente los **requerimientos"
    " directos** de insumos intermedios necesarios para generar un lempira de"
    " producción en el sector seleccionado, **y no constituyen multiplicadores"
    " de Leontief** (los cuales capturan efectos directos e indirectos a través"
    " de la matriz inversa)."
)
