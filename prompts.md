# Prompts y proceso de desarrollo de HN MIP-IA

**Proyecto:** HN MIP-IA — Explorador Intersectorial Ampliado de Honduras  
**Programa:** Máster en Machine Learning e Inteligencia Artificial — OBS Business School  
**Asignatura:** Fundamentos de Programación  
**Herramientas:** ChatGPT, Gemini, Google Colab, Python, GitHub y Streamlit  
**Fuente estadística:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013

---

## 1. Introducción y nota metodológica

HN MIP-IA se desarrolló mediante programación asistida por inteligencia artificial, en el contexto de la asignatura Fundamentos de Programación.

**Primera etapa — Google Colab.** Se prepararon instrucciones técnicas con apoyo de ChatGPT, se utilizó Gemini para generar código Python y se ejecutaron y comprobaron los resultados en Google Colab.

**Segunda etapa — GitHub y Streamlit.** El desarrollo continuó con bloques de código preparados y revisados con ChatGPT, incorporados al repositorio y probados en la aplicación publicada.

Posteriormente, Gemini también se integró como servicio de interpretación económica de resultados calculados por Python.

**Nota sobre la procedencia de los prompts.** Los textos originales de las primeras instrucciones no están disponibles en los historiales consultados. Por ello, los cinco prompts siguientes son **reconstrucciones retrospectivas**, basadas en el código, las capturas de ejecución y los resultados documentados. **No son transcripciones literales.** La única instrucción literal reproducida se identifica expresamente en la sección 5.

## 2. Prompt 1 — Exploración y preparación de la Matriz Insumo-Producto

**Etapa:** Google Colab. **Registro:** reconstrucción retrospectiva.

### Instrucción reconstruida

> Necesito preparar la Matriz Insumo-Producto de Honduras 2013, publicada por el Banco Central de Honduras, para desarrollar una aplicación de exploración intersectorial.
>
> Genera código Python compatible con Google Colab para cargar el archivo Excel, identificar las hojas disponibles y examinar la Tabla 12, correspondiente a la matriz de coeficientes técnicos.
>
> Utiliza pandas para inspeccionar las dimensiones, identificar las actividades económicas y localizar las filas y columnas de coeficientes. Comprueba que existan 95 actividades y revisa la correspondencia de sus nombres entre filas y columnas.
>
> No alteres los coeficientes originales. Presenta los resultados de las comprobaciones antes de continuar.

### Evidencia y resultado

La hoja «Tabla 12» tenía inicialmente **104 filas × 98 columnas**, incluidos encabezados y elementos auxiliares. Se identificaron **95 actividades económicas** y diferencias de denominación entre filas y columnas en las actividades **12, 86 y 87**. Para construir etiquetas consistentes se adoptaron los nombres de las columnas en ambas dimensiones, sin alterar los coeficientes numéricos.

**Aprendizaje:** la validación de datos económicos debe abarcar tanto los valores como las etiquetas y clasificaciones.

## 3. Prompt 2 — Exportación y validación del CSV

**Etapa:** Google Colab. **Registro:** reconstrucción retrospectiva.

### Instrucción reconstruida

> Extrae de la Tabla 12 una matriz de coeficientes técnicos de 95 × 95, con los nombres de las actividades como índices de filas y columnas.
>
> Convierte los coeficientes a valores numéricos y verifica que no haya datos faltantes. Exporta el resultado a `data/mip_honduras_2013.csv`.
>
> Vuelve a cargar el CSV y comprueba sus dimensiones, valores y etiquetas. Utiliza NumPy para verificar que los coeficientes exportados coincidan con los originales.
>
> Como prueba adicional, compara la suma de coeficientes de «Caña de azúcar» antes y después de exportar.

### Evidencia y resultado

Se creó `data/mip_honduras_2013.csv`. Las comprobaciones registradas mostraron:

- **Dimensiones:** 95 × 95.
- **Valores faltantes:** 0.
- **Coeficientes:** coincidencia mediante `np.allclose`.
- **Etiquetas:** conservación de los nombres y su orden.
- **Caña de azúcar:** suma original y exportada de **0.167802**.

**Aprendizaje:** crear un archivo no garantiza que la transformación haya conservado la integridad de los datos.

## 4. Prompt 3 — Generación de la Versión 0 en Streamlit

**Etapa:** Google Colab. **Registro:** reconstrucción retrospectiva.

### Instrucción reconstruida

> Desarrolla una aplicación web educativa en Python con Streamlit para explorar relaciones intersectoriales directas de Honduras, utilizando `data/mip_honduras_2013.csv`.
>
> Configura una página amplia con título y fuente estadística. Carga el CSV con pandas y la primera columna como índice. Valida las dimensiones 95 × 95 y que los 9,025 coeficientes sean numéricos y finitos.
>
> Permite seleccionar una actividad entre las 95 disponibles. Utiliza su **columna** para identificar proveedores directos, excluye coeficientes cero y muestra los diez mayores en una tabla y un gráfico horizontal.
>
> Calcula la suma de coeficientes y exprésala también en centavos de insumos intermedios directos por lempira de producción.
>
> Incluye una advertencia: los coeficientes representan requerimientos directos, **no multiplicadores de Leontief**. Gestiona errores de carga y validación mediante mensajes comprensibles.
>
> Genera el archivo `app.py` desde Google Colab utilizando `%%writefile`, para su posterior despliegue en Streamlit.

### Evidencia y resultado

La primera versión de `app.py` incluyó configuración, carga y validación, selección de actividad, cálculos, visualización y resumen metodológico. Se utilizó `@st.cache_data`, se verificó la sintaxis con `py_compile` y se prepararon `requirements.txt` y `README.md`.

Se creó una copia de seguridad `MIP-IA_Version0.zip` con los archivos de la versión inicial.

**Aprendizaje:** el código generado por IA requiere comprobación técnica y validación económica antes de su publicación.

## 5. Prompt 4 — Prueba inicial de la API de Gemini

**Etapa:** cierre del trabajo en Google Colab. **Registro:** reconstrucción retrospectiva, con una instrucción literal conservada.

### Instrucción reconstruida

> Comprueba la integración de Gemini desde Google Colab mediante el SDK `google-genai`.
>
> Recupera `GEMINI_API_KEY` de los secretos de Colab, sin mostrarla ni incorporarla al código. Inicializa el cliente y realiza una solicitud breve de explicación económica.
>
> Muestra la respuesta y captura los posibles errores sin revelar las credenciales.

### Instrucción literal conservada en el código de prueba

> Explica en dos oraciones qué representa un coeficiente técnico directo en una Matriz Insumo-Producto.

### Evidencia y resultado

La prueba con `gemini-3.6-flash` produjo una respuesta. Antes de modificar la aplicación se creó `app_respaldo_pre_gemini.py`. Después se descargó `app.py` desde Colab para continuar el desarrollo fuera del cuaderno.

**Aprendizaje:** conviene verificar los servicios externos de forma independiente y conservar una versión estable antes de integrarlos.

**Seguridad:** este documento no incluye la clave API, su longitud ni huellas derivadas de ella.

## 6. Prompt 5 — Ampliación, depuración y respaldo

**Etapa:** desarrollo directo en GitHub y pruebas en Streamlit. **Registro:** síntesis retrospectiva de varias instrucciones; **no representa un único prompt original**.

### Instrucciones reconstruidas

> Amplía HN MIP-IA sin perder las funcionalidades validadas de la versión inicial.
>
> Incorpora **Clientes directos**, utilizando las **filas** de la matriz para identificar las principales actividades usuarias de una actividad proveedora. Mantén las **columnas** para Proveedores directos.
>
> Organiza ambos análisis en pestañas, con tablas, gráficos y descargas CSV.
>
> Añade botones de interpretación con Gemini. Python debe calcular los resultados; Gemini solo debe explicarlos, sin inventar cifras ni confundir coeficientes directos con ventas, participaciones de mercado o multiplicadores de Leontief.
>
> Controla respuestas vacías, generaciones incompletas y errores de disponibilidad. Configura un modelo principal y uno alternativo, conservando las consultas cuantitativas cuando la API no esté disponible.
>
> Elimina mensajes internos de diagnóstico de la interfaz y evita exponer secretos.

### Evidencia y resultado

La aplicación ampliada incorporó los módulos **Proveedores directos** y **Clientes directos**, tablas, gráficos, exportación CSV e interpretación asistida por Gemini. Se configuró `gemini-3.6-flash` como modelo principal y `gemini-3.5-flash-lite` como respaldo.

Las pruebas incluyeron respuestas incompletas por límite de tokens y una comprobación del mecanismo de respaldo mediante la configuración temporal de un identificador inexistente para el modelo principal. También se corrigieron etiquetas, visualizaciones y mensajes técnicos visibles al usuario.

**Aprendizaje:** la programación asistida por IA es iterativa; exige revisar el código, probar casos límite y mantener independientes las funciones cuantitativas esenciales.

## 7. Resultado del proyecto

**Aplicación:** https://mip-ia-honduras.streamlit.app/  
**Repositorio:** https://github.com/maciz-mc/mip-ia-honduras

La versión académica permite explorar relaciones intersectoriales **directas** desde dos perspectivas: proveedores y clientes. Los cálculos se realizan con Python; Gemini ofrece interpretaciones económicas complementarias.

La comparación simultánea entre dos actividades, los multiplicadores de Leontief, los efectos indirectos y la optimización económica **no forman parte de esta versión**.

## 8. Reflexión final

El proyecto permitió experimentar dos modalidades de programación asistida por IA: primero, instrucciones elaboradas con ChatGPT, código generado con Gemini y pruebas en Google Colab; después, desarrollo y corrección de código con ChatGPT, integración en GitHub y comprobación en Streamlit.

La supervisión humana fue indispensable para verificar la orientación de filas y columnas, la integridad de los coeficientes y la interpretación económica. La IA facilitó el aprendizaje y aceleró el desarrollo, pero no sustituyó la comprensión del problema ni la validación de resultados.

---

*Nota documental: los cinco apartados de prompts son reconstrucciones retrospectivas. Solo la instrucción breve de prueba de Gemini se reproduce literalmente por estar conservada en el código de Colab.*
