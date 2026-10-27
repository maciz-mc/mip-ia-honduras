# Especificación técnica del producto

**Proyecto:** HN MIP-IA — Explorador Intersectorial Ampliado de Honduras  
**Versión del documento:** 1.0  
**Programa:** Máster en Machine Learning e Inteligencia Artificial — OBS Business School  
**Tecnologías:** Python, pandas, Streamlit y API de Gemini  
**Fuente de datos:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013

---

## 1. Problema y usuario

### Problema

La Matriz Insumo-Producto (MIP) de Honduras contiene información sobre las relaciones productivas entre las actividades económicas. Sin embargo, su estructura matricial y el conocimiento técnico requerido para interpretarla dificultan su utilización por personas que no están familiarizadas con el análisis insumo-producto.

HN MIP-IA busca facilitar la exploración de estas relaciones mediante una aplicación interactiva que transforma los coeficientes técnicos en tablas, gráficos y explicaciones económicas comprensibles.

### Usuarios

La aplicación está dirigida principalmente a:

- Estudiantes universitarios de economía y disciplinas relacionadas.
- Investigadores interesados en la estructura productiva hondureña.
- Profesionales que realizan análisis sectoriales.
- Personas interesadas en comprender las relaciones económicas entre actividades productivas.

No se requieren conocimientos de programación para utilizarla.

## 2. Qué hace el producto

HN MIP-IA permite explorar las relaciones intersectoriales directas de la economía hondureña utilizando una matriz de coeficientes técnicos de 95 actividades económicas.

La aplicación comprenderá cinco funcionalidades:

### 2.1. Exploración de proveedores directos

El usuario selecciona una actividad económica y obtiene sus diez principales proveedores de insumos intermedios directos, ordenados según sus coeficientes técnicos.

### 2.2. Exploración de clientes directos

El usuario selecciona una actividad proveedora y visualiza las actividades económicas que utilizan sus productos como insumos intermedios directos, ordenadas según los coeficientes técnicos correspondientes.

### 2.3. Comparación intersectorial

El usuario selecciona dos actividades económicas y compara sus estructuras de requerimientos directos de insumos, identificando proveedores comunes, diferencias y coeficientes relevantes.

### 2.4. Interpretación económica con inteligencia artificial

Mediante la API de Gemini, la aplicación genera explicaciones en lenguaje natural de los resultados obtenidos por los módulos cuantitativos.

La IA no realiza los cálculos económicos ni modifica los resultados numéricos.

### 2.5. Visualización y exportación

Los resultados se presentan mediante tablas y gráficos interactivos, con opciones para descargar los datos calculados en formato CSV.

## 3. Entradas y salidas

### Entradas

- Archivo CSV con la matriz de coeficientes técnicos de 95 × 95 actividades.
- Selección de una actividad económica para el análisis de proveedores o clientes.
- Selección de dos actividades para el módulo de comparación.
- Solicitud del usuario para generar una interpretación económica mediante Gemini.

### Salidas

- Tabla ordenada de los diez principales proveedores directos.
- Tabla ordenada de las principales actividades usuarias de los productos de una actividad seleccionada.
- Gráficos de barras para visualizar los coeficientes técnicos.
- Tablas y gráficos comparativos entre dos actividades.
- Interpretaciones económicas generadas mediante Gemini.
- Archivos CSV descargables con los resultados cuantitativos.

Los resultados deberán identificar claramente las actividades analizadas y la fuente de información.

## 4. La pieza de inteligencia artificial

La aplicación utilizará la API de Gemini como componente de interpretación económica.

### Función de Gemini

Transformar los resultados cuantitativos previamente calculados en explicaciones claras, estructuradas y comprensibles para el usuario.

### Información proporcionada a Gemini

El sistema enviará únicamente la información necesaria para interpretar el análisis seleccionado:

- Nombre de la actividad o actividades económicas.
- Tipo de análisis realizado.
- Resultados numéricos calculados por Python.
- Definiciones metodológicas pertinentes.
- Instrucciones que delimitan el alcance de la interpretación.

### Restricciones de la IA

Gemini deberá:

- Utilizar exclusivamente los resultados suministrados por la aplicación.
- Respetar los valores numéricos calculados.
- Diferenciar relaciones directas de efectos indirectos.
- Evitar afirmaciones causales no sustentadas.
- No inventar actividades, coeficientes ni resultados.
- Reconocer expresamente las limitaciones de la información disponible.

Las respuestas generadas se identificarán como interpretaciones asistidas por inteligencia artificial y no como resultados estadísticos adicionales.

## 5. Flujo del usuario

1. El usuario ingresa a HN MIP-IA mediante su dirección pública en Streamlit.
2. La aplicación carga y valida la matriz de coeficientes técnicos.
3. El usuario selecciona uno de los módulos de análisis.
4. Selecciona una o dos actividades económicas, según corresponda.
5. Python procesa la matriz y obtiene los resultados.
6. La aplicación presenta las tablas y visualizaciones.
7. Opcionalmente, el usuario solicita una interpretación con Gemini.
8. El usuario puede descargar los resultados cuantitativos en CSV.

La exploración cuantitativa deberá permanecer disponible aunque el servicio de Gemini presente errores o interrupciones.

## 6. Restricciones

### Restricciones técnicas

- Utilizar Python y bibliotecas compatibles con Streamlit Community Cloud.
- Mantener la matriz de datos dentro del repositorio del proyecto.
- Verificar que la matriz contenga 95 filas y 95 columnas, con valores numéricos válidos.
- No incorporar claves API directamente en el código fuente.
- Utilizar un mecanismo seguro de gestión de credenciales para Gemini.
- Gestionar los errores de conexión sin interrumpir el funcionamiento de los módulos cuantitativos.

### Restricciones metodológicas

- Utilizar exclusivamente la matriz de coeficientes técnicos del BCH correspondiente a 2013.
- Conservar la orientación correcta de filas y columnas de la matriz.
- Distinguir la intensidad de utilización de insumos de los valores monetarios de las transacciones.
- No presentar coeficientes técnicos como multiplicadores económicos.
- No inferir relaciones causales a partir de asociaciones matriciales.

### Restricciones de alcance

El proyecto corresponde a una aplicación educativa y exploratoria. No pretende sustituir un estudio económico sectorial completo ni producir recomendaciones automáticas de política económica.

## 7. Criterios de aceptación

Se considerará satisfactoria la versión académica cuando se verifique que:

1. La aplicación se ejecuta correctamente mediante su enlace público.
2. La matriz de 95 × 95 actividades se carga y valida.
3. El usuario puede seleccionar cualquiera de las 95 actividades económicas.
4. El módulo de proveedores identifica correctamente los diez mayores coeficientes técnicos de la actividad compradora seleccionada.
5. El módulo de clientes identifica correctamente las actividades que utilizan insumos de la actividad proveedora seleccionada.
6. La comparación entre dos actividades produce resultados coherentes con la matriz original.
7. Las tablas y gráficos representan fielmente los valores calculados.
8. Los archivos CSV descargados contienen los resultados correspondientes al análisis seleccionado.
9. Gemini genera interpretaciones a partir de los resultados calculados, sin alterar los valores.
10. La aplicación continúa funcionando en sus módulos cuantitativos cuando Gemini no está disponible.
11. No se publican claves API ni otras credenciales privadas en GitHub.
12. La documentación permite comprender, ejecutar y verificar el funcionamiento del producto.

## 8. Fuera de alcance

Para esta versión académica se excluyen expresamente:

- Cálculo de la inversa de Leontief.
- Multiplicadores de producción, ingreso o empleo.
- Encadenamientos productivos indirectos y totales.
- Modelos de programación lineal.
- Optimización de la estructura productiva.
- Simulaciones de política económica.
- Incorporación de matrices de otros años.
- Actualización automática de estadísticas económicas.
- Predicciones económicas generadas mediante IA.

Estas funcionalidades podrán evaluarse en una etapa posterior, una vez concluidos los cuatro documentos del estudio de optimización macroeconómica de Honduras.

## 9. Despliegue

### Plataforma

Streamlit Community Cloud.

### Repositorio

https://github.com/maciz-mc/mip-ia-honduras

### Aplicación publicada

https://mip-ia-honduras.streamlit.app/

### Componentes principales

- `app.py`: aplicación principal.
- `requirements.txt`: dependencias de Python.
- `README.md`: documentación del proyecto.
- `especificacion.md`: especificación técnica del producto.
- `AGENTS.md`: instrucciones para asistentes de programación.
- `data/`: archivos de datos utilizados por la aplicación.

### Mantenimiento

El desarrollo se realizará de manera incremental, preservando las funcionalidades previamente verificadas. Cada modificación deberá probarse antes de considerarse parte de una nueva versión estable.
