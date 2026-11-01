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

- **Modelo principal:** `gemini-3.6-flash`.
- **Modelo de respaldo:** `gemini-3.5-flash-lite`.

Sus identificadores se administran mediante las constantes `MODELO_GEMINI` y `MODELO_RESPALDO` de `app.py`.

### 4.3. Información proporcionada a Gemini

El sistema envía la información necesaria para interpretar el análisis seleccionado:

- Nombre de la actividad económica.
- Tipo de análisis: Proveedores o Clientes.
- Diez principales coeficientes técnicos directos.
- Suma de coeficientes de la columna completa, cuando corresponde al módulo de proveedores.
- Instrucciones metodológicas que delimitan el alcance de la interpretación.

### 4.4. Restricciones de la IA

Gemini debe:

- Utilizar exclusivamente los resultados suministrados por la aplicación.
- Respetar los valores numéricos calculados.
- Diferenciar relaciones directas de efectos indirectos.
- Evitar afirmaciones causales no sustentadas.
- No inventar actividades, coeficientes ni resultados.
- Reconocer las limitaciones de la información disponible.

Las respuestas generadas constituyen interpretaciones asistidas por inteligencia artificial y no resultados estadísticos adicionales.

### 4.5. Mecanismo automático de respaldo

La aplicación solicita inicialmente la interpretación al modelo principal.

Si este no produce una respuesta válida, el sistema intenta obtenerla mediante el modelo de respaldo.

Entre las situaciones contempladas se encuentran:

- Respuestas vacías.
- Respuestas incompletas por límite de generación.
- Errores de cuota o límite de solicitudes (429).
- Indisponibilidad del modelo solicitado (404).
- Indisponibilidad temporal del servicio (503).

Los errores de autenticación (401 y 403) se gestionan mediante mensajes específicos.

Si no se obtiene una respuesta válida, la aplicación informa al usuario sin interrumpir los módulos cuantitativos.

El mecanismo de respaldo mejora la continuidad operativa, pero no garantiza disponibilidad permanente ni elimina las restricciones de uso de la API.

### 4.6. Seguridad de credenciales

La clave `GEMINI_API_KEY` se administra mediante los secretos de Streamlit.

No debe incorporarse al código fuente, al repositorio público ni a los documentos de entrega.

## 5. Flujo del usuario

1. El usuario ingresa a HN MIP-IA mediante su dirección pública en Streamlit.
2. La aplicación carga y valida la matriz de coeficientes técnicos.
3. El usuario selecciona el módulo Proveedores directos o Clientes directos.
4. Selecciona una actividad económica.
5. Python procesa la columna o fila correspondiente y obtiene los resultados.
6. La aplicación presenta las tablas y visualizaciones.
7. Opcionalmente, el usuario solicita una interpretación con Gemini.
8. El sistema consulta el modelo principal y, cuando corresponde, intenta utilizar el modelo de respaldo.
9. El usuario recibe la interpretación o un mensaje comprensible si no fue posible generarla.
10. El usuario puede descargar los resultados cuantitativos en CSV.

La exploración cuantitativa permanece disponible aunque el servicio de Gemini presente errores o interrupciones.

## 6. Restricciones

### Restricciones técnicas

- Utilizar Python y bibliotecas compatibles con Streamlit Community Cloud.
- Mantener la matriz de datos dentro del repositorio del proyecto.
- Verificar que la matriz contenga 95 filas y 95 columnas, con valores numéricos válidos y finitos.
- Verificar la correspondencia de nombres y orden entre filas y columnas.
- No incorporar claves API directamente en el código fuente.
- Utilizar los secretos de Streamlit para gestionar las credenciales de Gemini.
- Gestionar los errores de conexión, autenticación y generación sin interrumpir los módulos cuantitativos.
- Conservar el mecanismo automático de respaldo entre modelos, salvo modificación expresamente autorizada.

### Restricciones metodológicas

- Utilizar exclusivamente la matriz de coeficientes técnicos del BCH correspondiente a 2013.
- Conservar la orientación correcta de filas y columnas de la matriz.
- Distinguir la intensidad de utilización de insumos de los valores monetarios de las transacciones.
- No presentar coeficientes técnicos como multiplicadores económicos.
- No inferir relaciones causales a partir de asociaciones matriciales.
- Realizar los cálculos económicos mediante Python, no mediante Gemini.

### Restricciones de alcance

HN MIP-IA constituye una iniciativa personal de investigación, aprendizaje y experimentación tecnológica, orientada a profundizar conocimientos en programación, inteligencia artificial y análisis de la estructura productiva de Honduras.

Su desarrollo tiene fines académicos y de perfeccionamiento profesional.

La aplicación es educativa y exploratoria. No pretende sustituir un estudio económico sectorial completo ni producir recomendaciones automáticas de política económica.

## 7. Criterios de aceptación

Se considerará satisfactoria la versión académica cuando se verifique que:

1. La aplicación se ejecuta correctamente mediante su enlace público.
2. La matriz de 95 × 95 actividades se carga y valida.
3. El usuario puede seleccionar cualquiera de las 95 actividades económicas.
4. El módulo de proveedores identifica correctamente los diez mayores coeficientes técnicos de la actividad compradora seleccionada.
5. El módulo de clientes identifica correctamente las diez principales actividades usuarias según los coeficientes de la fila seleccionada.
6. Las tablas y gráficos representan fielmente los valores calculados.
7. Los archivos CSV descargados contienen los resultados correspondientes al análisis seleccionado.
8. Gemini genera interpretaciones a partir de los resultados calculados, sin alterar los valores.
9. El sistema intenta utilizar el modelo de respaldo cuando el principal no produce una respuesta válida.
10. La aplicación continúa funcionando en sus módulos cuantitativos cuando Gemini no está disponible.
11. Los mensajes de error son comprensibles y no exponen información técnica interna innecesaria.
12. No se publican claves API ni otras credenciales privadas en GitHub.
13. La documentación permite comprender, ejecutar y verificar el funcionamiento del producto.

### Pruebas realizadas

Durante el desarrollo se efectuaron pruebas de los módulos de proveedores y clientes, de la generación de interpretaciones y de la recuperación mediante el modelo alternativo.

En particular, se verificó el mecanismo de respaldo mediante la configuración temporal de un identificador inexistente para el modelo principal, obteniéndose una interpretación a través del modelo alternativo.

También se identificaron respuestas incompletas por límites de generación, lo que motivó ajustes en el tratamiento de errores.

Las pruebas realizadas no equivalen a una garantía de disponibilidad permanente de los servicios externos de Gemini.

## 8. Fuera de alcance

Para esta versión académica se excluyen expresamente:

- Comparación intersectorial entre dos actividades.
- Cálculo de la inversa de Leontief.
- Multiplicadores de producción, ingreso o empleo.
- Encadenamientos productivos indirectos y totales.
- Modelos de programación lineal.
- Optimización de la estructura productiva.
- Simulaciones de política económica.
- Incorporación de matrices de otros años.
- Actualización automática de estadísticas económicas.
- Predicciones económicas generadas mediante IA.

Estas funcionalidades podrán evaluarse como posibles ampliaciones de la iniciativa personal de investigación y aprendizaje, mediante una revisión metodológica y técnica específica.

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

El desarrollo se realizará de manera incremental, preservando las funcionalidades previamente verificadas.

Cada modificación deberá probarse antes de considerarse parte de una nueva versión estable.

Los cambios en modelos de IA, metodología económica, estructura de datos o arquitectura de la aplicación requieren revisión y autorización del responsable del proyecto.
