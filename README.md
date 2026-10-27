# HN MIP-IA — Explorador Intersectorial Ampliado de Honduras

**Aplicación publicada:** https://mip-ia-honduras.streamlit.app/  
**Repositorio:** https://github.com/maciz-mc/mip-ia-honduras  
**Proyecto académico:** Máster en Machine Learning e Inteligencia Artificial, OBS Business School  
**Fuente estadística:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013, matriz de coeficientes técnicos de 95 × 95 actividades.

> **Estado del proyecto:** la versión inicial permite explorar los diez principales proveedores directos de una actividad, visualizar los resultados y descargarlos en CSV. Los módulos de clientes directos, comparación intersectorial e interpretación con Gemini corresponden al desarrollo previsto para el reto y **aún no se presentan como implementados**.

## Pitch

1. Estudiantes, investigadores y profesionales interesados en la economía hondureña encuentran dificultades para explorar e interpretar las relaciones productivas contenidas en una matriz de 95 × 95 actividades.
2. HN MIP-IA permite seleccionar actividades económicas y visualizar sus relaciones intersectoriales directas mediante tablas y gráficos, comenzando por los diez principales proveedores de insumos.
3. La integración prevista con Gemini aportará explicaciones económicas en lenguaje natural basadas exclusivamente en los resultados calculados por Python, sin sustituir los cálculos.
4. La versión inicial ha permitido comprobar la utilidad de seleccionar actividades, ordenar coeficientes técnicos y exportar resultados; las pruebas formales de la versión ampliada están pendientes.
5. Tras completar y probar la versión académica, la aplicación podrá revisarse a la luz de los cuatro documentos del estudio de optimización macroeconómica de Honduras, sin incorporar todavía esos modelos al reto.

## El problema

La Matriz Insumo-Producto del BCH permite estudiar las relaciones directas entre actividades económicas, pero su estructura dificulta la consulta por personas que no utilizan habitualmente herramientas matriciales. Sin una interfaz especializada, es necesario identificar manualmente filas y columnas, ordenar coeficientes y elaborar gráficos. HN MIP-IA facilita esa exploración y presenta resultados comprensibles, sin exigir conocimientos de programación. La inteligencia artificial se reserva para interpretar resultados calculados y no para producir cifras.

## Qué hace la app

### Disponible en la versión inicial

1. Seleccionar una de las 95 actividades económicas como **actividad compradora**.
2. Identificar sus **diez principales proveedores de insumos intermedios directos**, ordenados por coeficiente técnico.
3. Consultar la tabla y el gráfico de resultados.
4. Descargar los resultados en formato CSV.

### Funcionalidades previstas para la versión académica ampliada

1. **Clientes o actividades usuarias directas:** seleccionar una actividad proveedora y consultar qué actividades utilizan sus productos como insumos, según los coeficientes de la matriz.
2. **Comparación intersectorial:** seleccionar dos actividades compradoras y comparar sus estructuras de requerimientos directos.
3. **Interpretación asistida por Gemini:** solicitar una explicación de los resultados ya calculados, con advertencias sobre sus límites metodológicos.
4. **Visualización y exportación ampliadas:** presentar y descargar resultados de los nuevos módulos.

**Precisión metodológica:** las filas de la matriz corresponden a actividades proveedoras y las columnas a actividades compradoras. Los coeficientes técnicos expresan requerimientos directos por unidad de producción de la actividad compradora; no representan por sí mismos ventas, participaciones de mercado, multiplicadores de Leontief ni impactos totales.

## La pieza de IA

- **Qué usa:** está prevista la API de Gemini mediante el SDK `google-genai`; el modelo específico se elegirá y verificará durante la integración. **Gemini todavía no está integrado en la versión inicial.**
- **Por qué esa opción:** permite generar explicaciones en español de los resultados económicos calculados por Python y facilitar su comprensión a usuarios no especializados.
- **Qué datos recibe:** nombres de las actividades, tipo de consulta, resultados numéricos verificados y límites metodológicos necesarios para interpretarlos.
- **Qué no debe hacer:** inventar cifras, modificar coeficientes, calcular efectos indirectos, afirmar causalidad o presentar los coeficientes como volúmenes de ventas.
- **Qué pasa si falla:** el diseño exige un mensaje comprensible ante problemas de conexión, autenticación o cuota; los módulos cuantitativos deberán seguir funcionando. **Este comportamiento está pendiente de implementación y prueba.**
- **Seguridad:** la clave `GEMINI_API_KEY` se almacenará en los secretos de Streamlit y nunca en el repositorio, en capturas ni en conversaciones.

## Cómo la he construido

- **Herramientas de desarrollo:** Python, pandas, NumPy, Streamlit y GitHub. Se ha utilizado ChatGPT como asistente para la planificación, el diseño metodológico y la documentación del proyecto.
- **Despliegue:** Streamlit Community Cloud (ruta A del reto de OBS).
- **Especificación del producto:** [`especificacion.md`](especificacion.md).
- **Instrucciones para agentes de programación:** [`AGENTS.md`](AGENTS.md).
- **Prompts clave (3 a 5, texto literal):** pendiente de seleccionar y transcribir a partir de las conversaciones de desarrollo. No se incluyen frases reconstruidas como si fueran citas literales.
- **Qué se delegó al asistente:** apoyo en la definición del producto, la estructura documental y las propuestas de implementación.
- **Qué se revisó manualmente:** la coherencia económica de la matriz, la distinción entre relaciones directas y efectos indirectos, el alcance del reto y la revisión de los cambios antes del despliegue.

## Prueba y mejora

La siguiente tabla es un **plan de pruebas**, no un registro de resultados ya obtenidos. Se completará con evidencias después de desarrollar los módulos pendientes.

| Quién la probó | Qué probó | Qué pasó | Qué cambié |
|---|---|---|---|
| Responsable del proyecto | Selección de actividad y diez proveedores directos | Versión inicial funcional; pendiente registrar caso y evidencia de la prueba final | Pendiente de documentar |
| Pendiente | Selección de actividad proveedora y consulta de clientes directos | Pendiente de implementación y prueba | Pendiente |
| Pendiente | Comparación de dos actividades | Pendiente de implementación y prueba | Pendiente |
| Pendiente | Solicitud de interpretación con Gemini | Pendiente de integración y prueba | Pendiente |
| Pendiente | Error de conexión o cuota de Gemini | Pendiente de integración y prueba | Pendiente |

### Criterios de comprobación

- La matriz tiene 95 filas y 95 columnas y contiene valores numéricos válidos.
- Los proveedores se obtienen de la **columna** de la actividad compradora; las actividades usuarias, de la **fila** de la actividad proveedora.
- Las tablas, los gráficos y los CSV muestran resultados consistentes entre sí.
- Gemini solo interpreta los resultados calculados; si falla, la consulta cuantitativa continúa disponible.
- Ninguna clave privada aparece en el código ni en la documentación publicada.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para probar la futura integración de Gemini, configurar `GEMINI_API_KEY` en `.streamlit/secrets.toml` **solo en el equipo local**, excluido del control de versiones mediante `.gitignore`. En Streamlit Community Cloud, configurar la clave desde la administración de secretos de la aplicación. No es necesario disponer de una clave para utilizar los módulos cuantitativos actuales.

## Capturas y evidencias de la entrega

Pendiente de incorporar, sin mostrar credenciales:

1. **La aplicación funcionando:** selección de actividad, tabla y gráfico de proveedores.
2. **Caso límite o error:** mensaje mostrado ante una situación controlada, como indisponibilidad de Gemini.
3. **Trabajo con el asistente de IA:** captura de un prompt real y de la respuesta recibida durante el desarrollo.
4. **Prueba y mejora:** evidencia de una prueba y de la modificación realizada a partir de ella.

## Alcance posterior al reto

La ampliación hacia multiplicadores de Leontief, encadenamientos indirectos, simulaciones y optimización macroeconómica **no forma parte de esta versión académica**. Se evaluará después de concluir el estudio de optimización macroeconómica de Honduras y sus cuatro documentos, mediante una revisión específica de la metodología y de la aplicación.

---

**Documentación:** este README describe el estado inicial conocido y la versión académica planificada. Debe actualizarse con resultados, prompts literales, capturas y pruebas reales antes de la entrega final del curso.
