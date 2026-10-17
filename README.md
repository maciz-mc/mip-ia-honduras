# MIP-IA: Explorador de relaciones intersectoriales de Honduras

## 📋 Objetivo del Proyecto
**MIP-IA** es una aplicación educativa desarrollada como parte de la asignatura *Fundamentos de Programación (Python para IA)* de la maestría en Inteligencia Artificial (OBS Business School). Su objetivo principal es permitir a estudiantes, investigadores y profesionales explorar y analizar los requerimientos intermedios directos de las 95 actividades económicas de la economía hondureña.

## 📊 Fuente de Datos Oficial
La aplicación utiliza los datos publicados por el **Banco Central de Honduras (BCH)** correspondientes a la **Matriz Insumo-Producto de Honduras 2013**, específicamente la **Tabla 12 (DB)** (Matriz de coeficientes técnicos aplicada sobre la producción bruta total).

## ✨ Funcionalidades (Versión 0)
1. **Selección interactiva:** Permite elegir cualquiera de las 95 actividades económicas (industrias compradoras) de la economía hondureña mediante un menú desplegable.
2. **Top 10 de requerimientos directos:** Identifica, ordena y presenta en formato tabular los diez principales insumos requeridos por la actividad seleccionada.
3. **Visualización gráfica:** Muestra un gráfico de barras horizontal interactivo para facilitar la lectura de los coeficientes.
4. **Resumen cuantitativo:** Calcula la suma total de los coeficientes técnicos de la actividad, expresada tanto en valor decimal como en centavos de lempira de insumos intermedios directos por cada lempira de producción.

## ⚠️ Aclaración Metodológica
Los coeficientes presentados en esta herramienta reflejan estrictamente los **requerimientos directos** de insumos intermedios necesarios para generar un lempira de producción en el sector seleccionado. **No constituyen multiplicadores de Leontief** (los cuales capturan efectos directos e indirectos a través de la matriz inversa de Leontief).

## 🛠️ Tecnologías Utilizadas
* **Python**: Lenguaje de programación principal para la lógica y los cálculos económicos.
* **Pandas**: Manipulación, limpieza y procesamiento estructurado de matrices de datos.
* **NumPy**: Validación numérica estricta.
* **Streamlit**: Construcción de la interfaz gráfica web interactiva.

## 📁 Estructura del Repositorio
```text
mip-ia/
│
├── data/
│   └── mip_honduras_2013.csv   # Matriz DB depurada (95x95)
│
├── app.py                      # Interfaz web y lógica de presentación (Streamlit)
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación principal

## 🚀 Instrucciones de Ejecución y Despliegue

### 1. Ejecución local

Para ejecutar la aplicación en una computadora con Python instalado:

1. Descargar o clonar el repositorio.
2. Instalar las dependencias:

    pip install -r requirements.txt

3. Iniciar Streamlit:

    streamlit run app.py

### 2. Despliegue en Streamlit Community Cloud

1. Publicar los archivos del proyecto en un repositorio de GitHub.
2. Acceder a Streamlit Community Cloud.
3. Conectar el repositorio de GitHub.
4. Seleccionar la rama principal y el archivo app.py.
5. Desplegar y comprobar el funcionamiento de la aplicación.

## 📌 Estado del Desarrollo

**Versión actual:** Versión 0. Código implementado y validado
sintácticamente en Google Colab. Pendiente de pruebas de funcionamiento
en Streamlit y despliegue público.

**Fases futuras:** Integración de la API de Gemini para generar
interpretaciones económicas de los resultados cuantitativos.
