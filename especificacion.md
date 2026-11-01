# Especificación técnica del producto

**Proyecto:** HN MIP-IA — Explorador Intersectorial Ampliado de Honduras  
**Versión del documento:** 1.1  
**Programa:** Máster en Machine Learning e Inteligencia Artificial — OBS Business School  
**Tecnologías:** Python, pandas, NumPy, Streamlit, Altair y API de Gemini  
**Fuente de datos:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013

---

## 1. Problema y usuario

### Problema

La Matriz Insumo-Producto (MIP) de Honduras contiene información sobre las relaciones productivas entre las actividades económicas. Sin embargo, su estructura matricial y el conocimiento técnico requerido para interpretarla dificultan su utilización por personas que no están familiarizadas con el análisis insumo-producto.

HN MIP-IA facilita la exploración de estas relaciones mediante una aplicación interactiva que transforma los coeficientes técnicos en tablas, gráficos y explicaciones económicas comprensibles.

El proyecto constituye una iniciativa personal de investigación, aprendizaje y experimentación tecnológica, orientada a profundizar conocimientos en programación, inteligencia artificial y análisis de la estructura productiva de Honduras.

### Usuarios

La aplicación está dirigida principalmente a:

- Estudiantes universitarios de economía y disciplinas relacionadas.
- Investigadores interesados en la estructura productiva hondureña.
- Profesionales que realizan análisis sectoriales.
- Personas interesadas en comprender las relaciones económicas entre actividades productivas.

No se requieren conocimientos de programación para utilizarla.

## 2. Qué hace el producto

HN MIP-IA permite explorar las relaciones intersectoriales directas de la economía hondureña utilizando una matriz de coeficientes técnicos de 95 actividades económicas.

La versión implementada comprende tres funcionalidades principales.

### 2.1. Exploración de proveedores directos

El usuario selecciona una actividad económica compradora y obtiene sus diez principales proveedores de insumos intermedios directos, ordenados según sus coeficientes técnicos.

El módulo utiliza la columna correspondiente a la actividad seleccionada y presenta:

- Tabla de los diez principales proveedores directos.
- Gráfico de barras con los coeficientes técnicos.
- Suma de los coeficientes de la columna completa.
- Expresión de los requerimientos intermedios directos en centavos por lempira de producción.
- Descarga de resultados en formato CSV.

### 2.2. Exploración de clientes directos

El usuario selecciona una actividad proveedora y visualiza las diez principales actividades económicas que utilizan sus productos como insumos intermedios directos.

El módulo utiliza la fila correspondiente a la actividad seleccionada y presenta:

- Tabla de las diez principales actividades usuarias.
- Gráfico de barras con los coeficientes técnicos.
- Descarga de resultados en formato CSV.

Los coeficientes se interpretan como intensidad técnica de utilización del producto de la actividad proveedora, no como volúmenes de ventas ni participaciones de mercado.

### 2.3. Interpretación económica con inteligencia artificial

Ambos módulos incorporan interpretación económica asistida por Gemini.

La aplicación envía los resultados previamente calculados mediante Python y solicita una explicación en lenguaje natural.

La IA no realiza los cálculos económicos ni modifica los resultados numéricos.

La integración incorpora un mecanismo automático de respaldo entre dos modelos para mejorar la continuidad del servicio.

## 3. Entradas y salidas

### Entradas

- Archivo CSV con la matriz de coeficientes técnicos de 95 × 95 actividades.
- Selección de una actividad económica para el análisis de proveedores o clientes.
- Solicitud del usuario para generar una interpretación económica mediante Gemini.

### Salidas

- Tabla ordenada de los diez principales proveedores directos.
- Tabla ordenada de las diez principales actividades usuarias de los productos de una actividad seleccionada.
- Gráficos de barras para visualizar los coeficientes técnicos.
- Suma de coeficientes y expresión monetaria por unidad de producción en el módulo de proveedores.
- Interpretaciones económicas generadas mediante Gemini.
- Archivos CSV descargables con los resultados cuantitativos.
- Mensajes comprensibles cuando no es posible obtener una interpretación de IA.

Los resultados identifican las actividades analizadas y la fuente de información.

## 4. La pieza de inteligencia artificial

La aplicación utiliza la API de Gemini como componente de interpretación económica, mediante el SDK `google-genai`.

### 4.1. Función de Gemini

Transformar los resultados cuantitativos previamente calculados en explicaciones claras, estructuradas y comprensibles para el usuario.

La inteligencia artificial desempeña una función interpretativa y no sustituye los procedimientos cuantitativos.

### 4.2. Modelos utilizados

La aplicación dispone de dos modelos configurados:

- **Modelo principal:** `gemini
