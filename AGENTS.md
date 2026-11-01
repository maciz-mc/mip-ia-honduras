# AGENTS.md · HN MIP-IA — Explorador Intersectorial Ampliado de Honduras

> Instrucciones para asistentes y agentes de programación que colaboren en este repositorio. Antes de modificar el código, leer `especificacion.md` y este archivo. Para Claude Code puede crearse `CLAUDE.md` con la línea `Sigue las instrucciones de AGENTS.md`; para Gemini CLI, `GEMINI.md` con la misma línea.

## Qué es este proyecto

HN MIP-IA es una aplicación educativa de exploración de las relaciones intersectoriales directas de la economía hondureña, basada en la Matriz Insumo-Producto 2013 del Banco Central de Honduras (BCH), dirigida a estudiantes, investigadores y profesionales.

La versión académica implementada comprende:

- **Proveedores directos:** identificación de los diez principales proveedores de insumos intermedios de una actividad compradora.
- **Clientes directos:** identificación de las diez principales actividades usuarias de los productos de una actividad proveedora.
- **Visualización y exportación:** tablas, gráficos y descarga de resultados en CSV.
- **Interpretación asistida por Gemini:** generación de explicaciones económicas a partir de resultados calculados mediante Python.
- **Respaldo automático de IA:** utilización de un segundo modelo cuando el principal no produce una respuesta válida.

La comparación intersectorial entre actividades y los modelos de optimización macroeconómica no forman parte de la versión implementada.

## Cómo está hecho

- **Lenguaje:** Python; utilizar una versión compatible con Streamlit Community Cloud.
- **Interfaz y despliegue:** Streamlit / Streamlit Community Cloud.
- **Procesamiento cuantitativo:** pandas y, cuando corresponda, NumPy.
- **Visualización:** Altair.
- **Inteligencia artificial:** API de Gemini mediante el SDK `google-genai`.
- **Modelo principal:** `gemini-3.6-flash`.
- **Modelo de respaldo:** `gemini-3.5-flash-lite`.
- **Archivos principales:** `app.py`, `requirements.txt`, `README.md`, `especificacion.md`, `AGENTS.md` y directorio `data/`.
- **Especificación funcional y metodológica:** `especificacion.md`.
- **Repositorio:** https://github.com/maciz-mc/mip-ia-honduras
- **Aplicación:** https://mip-ia-honduras.streamlit.app/

Los identificadores de los modelos se administran mediante las constantes `MODELO_GEMINI` y `MODELO_RESPALDO` definidas en `app.py`.

Antes de modificar estas constantes, comprobar que los modelos estén disponibles para la API utilizada.

## Reglas

### Seguridad y privacidad

1. La clave de Gemini debe almacenarse **siempre** en los secretos de Streamlit (`st.secrets`). Para pruebas locales, utilizar `.streamlit/secrets.toml`, excluido de Git mediante `.gitignore`. Nunca colocar credenciales en código, documentación, commits, capturas ni conversaciones.

2. Las llamadas a la API deben estar protegidas mediante manejo de excepciones y producir mensajes comprensibles ante errores de autenticación, cuota, disponibilidad o generación.

3. Si Gemini falla, los cálculos, tablas, gráficos y archivos CSV deben continuar funcionando.

4. No incorporar datos personales reales ni enviar información privada a servicios externos.

### Integridad económica y estadística

5. Utilizar la matriz de coeficientes técnicos de la MIP del BCH 2013, con **95 actividades por 95 actividades**. Validar dimensiones, etiquetas, tipos numéricos y valores finitos antes de calcular.

6. Respetar la orientación de la matriz: **filas = actividades proveedoras de insumos; columnas = actividades compradoras o usuarias**. Para proveedores de una actividad, analizar su columna; para clientes o actividades usuarias de un proveedor, analizar su fila.

7. Los coeficientes técnicos expresan requerimientos directos por unidad de producción de la actividad compradora. **No son valores monetarios de ventas ni participaciones de mercado**. Al ordenar actividades usuarias de un proveedor por coeficientes, describirlo como intensidad técnica de uso, no como clasificación por volumen de compras.

8. No confundir coeficientes directos con multiplicadores de Leontief, efectos indirectos, impactos totales ni causalidad económica.

9. Los cálculos y ordenamientos deben realizarse mediante Python; Gemini solo explica resultados ya calculados y verificados. No pedirle a Gemini que invente, estime o corrija cifras.

10. Conservar la precisión numérica de los cálculos y aplicar redondeos únicamente para presentación, cuando corresponda. Etiquetar claramente las unidades y la fuente.

### Integración y respaldo de Gemini

11. Mantener la configuración de los dos modelos mediante las constantes `MODELO_GEMINI` y `MODELO_RESPALDO`.

12. Consultar inicialmente el modelo principal. Si no produce una respuesta válida, intentar automáticamente con el modelo de respaldo.

13. Considerar como respuestas no válidas aquellas que estén vacías o cuya generación haya terminado sin completar la interpretación.

14. Conservar el manejo de errores HTTP relevantes, incluyendo autenticación (401 y 403), cuota (429), modelo no disponible (404) e indisponibilidad temporal (503).

15. No mostrar al usuario información interna de diagnóstico, identificadores técnicos de errores ni detalles de configuración de la API.

16. Si ambos modelos fallan, presentar una advertencia comprensible y mantener disponibles las funcionalidades cuantitativas.

17. No asumir que el modelo de respaldo dispone de una cuota independiente. La disponibilidad y el consumo dependen de las condiciones aplicables a cada modelo y a la API utilizada.

18. No modificar identificadores de modelos, parámetros de generación, instrucciones del sistema ni mecanismos de respaldo sin autorización expresa.

### Desarrollo y documentación

19. Todos los textos visibles para el usuario estarán en español y serán comprensibles para personas sin formación técnica especializada.

20. Hacer cambios pequeños y verificables: **una funcionalidad o corrección por petición**. Explicar qué se cambió, por qué y cómo se comprobó.

21. Antes de editar, revisar el código y los datos existentes; preservar lo que ya funciona y evitar reescrituras innecesarias.

22. Si se añade una biblioteca, registrarla en `requirements.txt` e indicar el motivo.

23. Mantener `README.md` y `especificacion.md` consistentes con el comportamiento real de la aplicación; no declarar como implementada una función que todavía esté planificada.

24. No borrar ni reescribir íntegramente `README.md`, cambiar la arquitectura, sustituir modelos de IA ni modificar la fuente de datos sin aprobación expresa.

25. **No hacer `git push`, fusionar cambios ni desplegar la aplicación sin revisión y autorización del responsable del proyecto.**

## Cómo comprobar que funciona

### Comprobación técnica

- Ejecutar localmente con `streamlit run app.py`, con las dependencias de `requirements.txt` instaladas.
- Para probar Gemini localmente, configurar la clave únicamente en `.streamlit/secrets.toml`.
- Tras una modificación aprobada, comprobar el despliegue en Streamlit Community Cloud.
- Verificar que los resultados numéricos coincidan con las operaciones realizadas directamente sobre el CSV original.
- Comprobar que los módulos cuantitativos funcionan incluso cuando Gemini no está disponible.

### Casos de prueba mínimos (entrada → resultado esperado)

1. **Seleccionar una actividad compradora** → se muestran los diez mayores coeficientes de su columna, con nombres y valores correctos.

2. **Seleccionar una actividad proveedora** → se identifican correctamente las actividades usuarias de su fila, sin interpretar los coeficientes como ventas.

3. **Descargar un CSV** → el archivo contiene las mismas actividades y valores que la tabla correspondiente.

4. **Solicitar interpretación a Gemini** → el texto se basa exclusivamente en los resultados calculados y reconoce sus límites metodológicos.

5. **Configurar temporalmente un identificador inexistente para el modelo principal** → el sistema intenta utilizar el modelo de respaldo y puede obtener una interpretación válida.

6. **Simular una respuesta incompleta** → el sistema intenta recuperar la generación mediante el respaldo y, si no obtiene una respuesta válida, muestra una advertencia comprensible.

7. **Simular error o cuota agotada de Gemini** → aparece un mensaje claro y siguen operativos los módulos cuantitativos.

8. **Matriz incompleta, no numérica o de dimensiones incorrectas** → se detiene el cálculo afectado y se presenta un error comprensible.

Las pruebas deben realizarse sin exponer claves privadas y sin introducir modificaciones permanentes que comprometan el funcionamiento de la aplicación.

## Qué no hacer

- No exponer claves API ni solicitar que se compartan por chat.
- No alterar la orientación de la matriz ni modificar silenciosamente los coeficientes.
- No usar Gemini para realizar los cálculos económicos.
- No presentar coeficientes técnicos como ventas totales o participaciones de mercado.
- No introducir multiplicadores de Leontief, simulaciones, optimización macroeconómica u otras funciones excluidas de la versión académica.
- No inventar datos, resultados, fuentes ni capacidades implementadas.
- No borrar ni reescribir el README sin consultar.
- No cambiar modelos de Gemini ni la arquitectura sin consultar.
- No eliminar el mecanismo de respaldo automático sin autorización.
- No hacer push ni desplegar sin aprobación.

## Alcance futuro

Después de concluir los cuatro documentos del estudio de optimización macroeconómica de Honduras, podrá evaluarse una ampliación analítica.

Entre las posibles funcionalidades futuras se encuentran la comparación intersectorial, los multiplicadores de Leontief, los encadenamientos indirectos y los modelos de simulación y optimización.

**Estas ampliaciones no forman parte del reto académico actual** y requieren una nueva revisión de la especificación antes de desarrollarse.
