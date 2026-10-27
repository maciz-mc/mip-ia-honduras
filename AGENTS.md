# AGENTS.md · HN MIP-IA — Explorador Intersectorial Ampliado de Honduras

> Instrucciones para asistentes y agentes de programación que colaboren en este repositorio. Antes de modificar el código, leer `especificacion.md` y este archivo. Para Claude Code puede crearse `CLAUDE.md` con la línea `Sigue las instrucciones de AGENTS.md`; para Gemini CLI, `GEMINI.md` con la misma línea.

## Qué es este proyecto

HN MIP-IA es una aplicación educativa de exploración de las relaciones intersectoriales directas de la economía hondureña, basada en la Matriz Insumo-Producto 2013 del Banco Central de Honduras (BCH), dirigida a estudiantes, investigadores y profesionales.

La versión académica del reto de OBS comprende: proveedores directos, clientes directos, comparación entre actividades, interpretación asistida por Gemini y visualización/exportación de resultados. **No todas estas funciones están implementadas todavía**; consultar el estado real del código antes de proponer cambios.

## Cómo está hecho

- Lenguaje: Python; usar una versión compatible con Streamlit Community Cloud (referencia académica: Python 3.12).
- Interfaz y despliegue (ruta A): Streamlit / Streamlit Community Cloud.
- Procesamiento cuantitativo: pandas y, cuando corresponda, NumPy.
- IA prevista: API de Gemini mediante el SDK `google-genai`. La integración está pendiente; al implementarla, centralizar el identificador del modelo en una constante `MODELO` de `app.py` y verificar que el modelo elegido esté disponible.
- Archivos principales: `app.py`, `requirements.txt`, `README.md`, `especificacion.md`, `AGENTS.md` y directorio `data/`.
- Especificación funcional y metodológica: [`especificacion.md`](especificacion.md).
- Repositorio: https://github.com/maciz-mc/mip-ia-honduras
- Aplicación: https://mip-ia-honduras.streamlit.app/

## Reglas

### Seguridad y privacidad

1. La clave de Gemini debe almacenarse **siempre** en los secretos de Streamlit (`st.secrets`, ruta A). Para pruebas locales, usar `.streamlit/secrets.toml` excluido de Git mediante `.gitignore`. Nunca colocar credenciales en el código, documentación, commits, capturas ni conversaciones.
2. Toda llamada a la API debe estar dentro de `try/except` y producir mensajes comprensibles si hay errores de conexión, autenticación, cuota o disponibilidad.
3. Si Gemini falla, la exploración cuantitativa debe seguir funcionando.
4. No incorporar datos personales reales ni enviar información privada a servicios externos.

### Integridad económica y estadística

5. Utilizar la matriz de coeficientes técnicos de la MIP del BCH 2013, con **95 actividades por 95 actividades**. Validar dimensiones, etiquetas, tipos numéricos y valores finitos antes de calcular.
6. Respetar la orientación de la matriz: **filas = actividades proveedoras de insumos; columnas = actividades compradoras o usuarias**. Para proveedores de una actividad, analizar su columna; para clientes o actividades usuarias de un proveedor, analizar su fila.
7. Los coeficientes técnicos expresan requerimientos directos por unidad de producción de la actividad compradora. **No son valores monetarios de ventas ni participaciones de mercado**. Al ordenar actividades usuarias de un proveedor por coeficientes, describirlo como intensidad técnica de uso, no como clasificación por volumen de compras.
8. No confundir coeficientes directos con multiplicadores de Leontief, efectos indirectos, impactos totales ni causalidad económica.
9. Los cálculos, ordenamientos y comparaciones deben realizarse mediante Python; Gemini solo explica resultados ya calculados y verificados. No pedirle a Gemini que invente, estime o corrija cifras.
10. Conservar la precisión numérica de los cálculos y aplicar redondeos únicamente para presentación, cuando corresponda. Etiquetar claramente las unidades y la fuente.

### Desarrollo y documentación

11. Todos los textos visibles para el usuario estarán en español y serán comprensibles para personas sin formación técnica especializada.
12. Hacer cambios pequeños y verificables: **una funcionalidad o corrección por petición**. Explicar qué se cambió, por qué y cómo se comprobó.
13. Antes de editar, revisar el código y los datos existentes; preservar lo que ya funciona y evitar reescrituras innecesarias.
14. Si se añade una biblioteca, registrarla en `requirements.txt` e indicar el motivo.
15. Mantener `README.md` y `especificacion.md` consistentes con el comportamiento real de la aplicación; no declarar como implementada una función que todavía esté planificada.
16. No borrar ni reescribir íntegramente `README.md`, cambiar la arquitectura, sustituir el modelo de IA ni modificar la fuente de datos sin aprobación expresa.
17. **No hacer `git push`, fusionar cambios ni desplegar la aplicación sin revisión y autorización del responsable del proyecto.**

## Cómo comprobar que funciona

### Comprobación técnica

- Ejecutar localmente con `streamlit run app.py`, con las dependencias de `requirements.txt` instaladas.
- Para probar Gemini localmente, configurar la clave únicamente en `.streamlit/secrets.toml`; no incluir ese archivo en el repositorio.
- Tras una modificación aprobada, comprobar el despliegue en Streamlit Community Cloud.
- Verificar que los resultados numéricos coincidan con las operaciones realizadas directamente sobre el CSV original.

### Casos de prueba mínimos (entrada → resultado esperado)

1. **Seleccionar una actividad compradora** → se muestran los diez mayores coeficientes de su columna, con nombres y valores correctos.
2. **Seleccionar una actividad proveedora** → se identifican correctamente las actividades usuarias de su fila, sin interpretar los coeficientes como ventas.
3. **Seleccionar dos actividades** → la comparación presenta los coeficientes de ambas de manera consistente, incluidos proveedores comunes y diferencias.
4. **Descargar un CSV** → el archivo contiene las mismas actividades y valores que la tabla correspondiente.
5. **Solicitar interpretación a Gemini** → el texto se basa exclusivamente en los resultados calculados y reconoce sus límites metodológicos.
6. **Simular error o cuota agotada de Gemini** → aparece un mensaje claro y siguen operativos los módulos cuantitativos.
7. **Probar una consulta ajena a la MIP o a los resultados disponibles** → la IA explica cortésmente que está fuera del alcance, sin inventar información.
8. **Matriz incompleta, no numérica o de dimensiones incorrectas** → se detiene el cálculo afectado y se presenta un error comprensible.

Los casos de prueba de módulos todavía no desarrollados son **criterios de aceptación futuros**, no evidencia de funcionamiento actual.

## Qué no hacer

- No exponer claves API ni solicitar que se compartan por chat.
- No alterar la orientación de la matriz ni modificar silenciosamente los coeficientes.
- No usar Gemini para realizar los cálculos económicos.
- No introducir multiplicadores de Leontief, simulaciones, optimización macroeconómica u otras funciones excluidas de la versión académica.
- No inventar datos, resultados, fuentes ni capacidades ya implementadas.
- No borrar ni reescribir el README sin consultar.
- No cambiar el modelo de Gemini ni la arquitectura sin consultar.
- No hacer push ni desplegar sin aprobación.

## Alcance futuro

Después de concluir los cuatro documentos del estudio de optimización macroeconómica de Honduras, podrá evaluarse una ampliación analítica. **Esa ampliación no forma parte del reto académico actual** y requiere una nueva revisión de la especificación antes de desarrollarse.
