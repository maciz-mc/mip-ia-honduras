# HN MIP-IA — Explorador Intersectorial Ampliado de Honduras

**Aplicación publicada:** https://mip-ia-honduras.streamlit.app/  
**Repositorio:** https://github.com/maciz-mc/mip-ia-honduras  
**Proyecto académico:** Máster en Machine Learning e Inteligencia Artificial, OBS Business School  
**Fuente estadística:** Banco Central de Honduras (BCH), Matriz Insumo-Producto 2013, Tabla 12 (DB), matriz de coeficientes técnicos de 95 × 95 actividades.

> **Estado del proyecto:** aplicación desplegada y funcional, con dos módulos de exploración intersectorial —Proveedores directos y Clientes directos— e interpretación económica asistida por Gemini. Incorpora un mecanismo automático de respaldo entre dos modelos de IA para mejorar la continuidad del servicio.

## Pitch

1. La Matriz Insumo-Producto de Honduras contiene información relevante sobre las relaciones productivas entre 95 actividades económicas, pero su estructura matricial dificulta la exploración por usuarios que no emplean habitualmente herramientas de análisis económico.

2. HN MIP-IA facilita la identificación de proveedores y clientes directos mediante una interfaz interactiva que presenta coeficientes técnicos, clasificaciones de las diez principales relaciones intersectoriales, tablas y gráficos.

3. La integración con Gemini permite generar interpretaciones económicas en lenguaje natural a partir de resultados calculados previamente mediante Python. La IA cumple una función explicativa y no sustituye los procedimientos cuantitativos.

4. La aplicación fue sometida a pruebas de funcionamiento, revisión de resultados y diagnóstico de errores de generación. Como mejora, se incorporó un modelo alternativo que se consulta automáticamente cuando el principal no produce una respuesta válida.

5. El proyecto constituye una herramienta académica de exploración de la estructura productiva hondureña. Su eventual ampliación hacia modelos de optimización macroeconómica requerirá un desarrollo metodológico independiente.

## El problema

La Matriz Insumo-Producto del Banco Central de Honduras permite examinar las relaciones directas entre las actividades económicas del país. Sin embargo, su utilización requiere identificar filas y columnas, interpretar coeficientes técnicos, ordenar resultados y construir representaciones gráficas.

HN MIP-IA simplifica estas operaciones mediante una aplicación web desarrollada con Python y Streamlit.

El usuario puede seleccionar una actividad económica y examinar tanto su estructura de compras intermedias como las actividades que utilizan sus productos en sus propios procesos productivos.

La integración de inteligencia artificial facilita la interpretación económica de los resultados, manteniendo separados los cálculos cuantitativos y la generación de explicaciones.

## Qué hace la app

### 1. Proveedores directos

Permite seleccionar una de las 95 actividades económicas como actividad compradora y examinar su estructura de requerimientos intermedios directos.

El módulo presenta:

- Las diez principales actividades proveedoras, ordenadas por coeficiente técnico.
- Una tabla de resultados y su representación gráfica.
- La suma de los coeficientes técnicos de la columna seleccionada.
- La expresión de los requerimientos intermedios directos en centavos por lempira de producción.
- La descarga de resultados en formato CSV.
- La interpretación económica asistida por Gemini.

El análisis se realiza utilizando las **columnas de la matriz**, correspondientes a las actividades compradoras.

### 2. Clientes directos

Permite seleccionar una actividad económica proveedora e identificar las principales actividades que utilizan sus productos como insumos intermedios.

El módulo presenta:

- Las diez principales actividades compradoras o usuarias directas.
- Una tabla de coeficientes técnicos y su representación gráfica.
- La descarga de resultados en formato CSV.
- La interpretación económica asistida por Gemini.

El análisis utiliza las **filas de la matriz**, correspondientes a las actividades proveedoras.

### 3. Interpretación económica asistida por IA

Ambos módulos incorporan un botón para generar una interpretación económica de los resultados.

La aplicación proporciona a Gemini la actividad seleccionada, el tipo de análisis y los coeficientes técnicos calculados por Python.

El modelo genera una explicación en español, orientada a facilitar la comprensión de las relaciones productivas identificadas.

### Precisión metodológica

Los coeficientes técnicos expresan requerimientos directos de insumos por unidad de producción de la actividad compradora.

En el módulo de Clientes directos, los coeficientes permiten identificar la intensidad con que distintas actividades utilizan el producto de la actividad proveedora, pero no representan cantidades totales vendidas ni participaciones de mercado.

Los resultados corresponden a relaciones directas y no constituyen estimaciones de efectos indirectos, multiplicadores de Leontief o impactos económicos totales.

## La pieza de IA

### Tecnología utilizada

La aplicación utiliza la API de Gemini mediante el SDK `google-genai`.

Se configuraron dos modelos:

- **Modelo principal:** `gemini-3.6-flash`.
- **Modelo de respaldo:** `gemini-3.5-flash-lite`.

Ambos se utilizan para generar interpretaciones económicas a partir de los resultados obtenidos mediante Python.

### Mecanismo de respaldo automático

La aplicación intenta inicialmente obtener una interpretación mediante el modelo principal.

Cuando este no genera una respuesta válida, el programa puede realizar automáticamente un segundo intento utilizando el modelo de respaldo.

El mecanismo contempla situaciones como respuestas vacías, generación incompleta, indisponibilidad del servicio y determinados errores de acceso al modelo.

Si ninguno de los dos modelos produce una interpretación válida, la aplicación presenta un mensaje comprensible para el usuario.

Los cálculos, tablas, gráficos y archivos CSV permanecen disponibles independientemente del funcionamiento de Gemini.

El mecanismo de respaldo mejora la resiliencia del servicio, aunque no garantiza disponibilidad permanente ni elimina las restricciones de cuota de la API.

### Función de Gemini

Gemini recibe información estructurada sobre los resultados calculados previamente:

- Tipo de análisis: Proveedores o Clientes.
- Actividad económica seleccionada.
- Diez principales coeficientes técnicos directos.
- Suma de coeficientes de la columna completa, cuando corresponde al módulo de Proveedores.

Las instrucciones del sistema orientan al modelo para producir explicaciones económicas claras, rigurosas y accesibles.

Gemini no debe inventar cifras, modificar coeficientes, atribuir causalidad no demostrada ni presentar los resultados como ventas totales o efectos indirectos.

### Seguridad

La clave privada `GEMINI_API_KEY` se administra mediante los secretos de Streamlit y no debe incorporarse al repositorio público.

Las solicitudes de interpretación utilizan la clave configurada por el responsable de la aplicación. Por tanto, el consumo de la API está sujeto a las cuotas y condiciones de los modelos utilizados.

## Cómo la he construido

### Herramientas

- **Python:** procesamiento de datos y cálculos.
- **pandas y NumPy:** manipulación y validación de la matriz.
- **Streamlit:** desarrollo de la interfaz interactiva.
- **Altair:** representación gráfica.
- **Google Gemini:** interpretación económica asistida por IA.
- **GitHub:** almacenamiento y control de versiones.
- **Streamlit Community Cloud:** publicación de la aplicación.
- **ChatGPT:** asistencia en planificación, programación, revisión metodológica, depuración y documentación.

### Metodología de desarrollo

El proyecto comenzó con la preparación y validación de la Matriz Insumo-Producto 2013 del BCH.

Se verificó la correspondencia entre filas y columnas, la dimensión de 95 × 95 actividades y la consistencia numérica de los coeficientes.

Posteriormente se desarrolló el módulo de Proveedores directos, seguido por el módulo de Clientes directos.

Una vez implementadas las funcionalidades cuantitativas, se incorporó Gemini para interpretar los resultados.

Durante las pruebas se identificaron problemas de disponibilidad de modelos, respuestas incompletas y límites de generación. Estos hallazgos motivaron la incorporación del mecanismo automático de respaldo y la mejora de los mensajes dirigidos al usuario.

### Participación del asistente de IA

ChatGPT se utilizó como herramienta de apoyo para formular alternativas de implementación, revisar código, diagnosticar errores y mejorar la documentación.

Las decisiones metodológicas, la validación económica y la aceptación de los cambios correspondieron al responsable del proyecto.

**Prompts literales utilizados durante el desarrollo:** pendientes de seleccionar y transcribir a partir de las conversaciones originales. No se presentan reconstrucciones como citas textuales.

### Documentación complementaria

- [Especificación del producto](especificacion.md)
- [Instrucciones para agentes de programación](AGENTS.md)

## Prueba y mejora

Las pruebas se realizaron sobre la aplicación publicada en Streamlit, utilizando diferentes actividades económicas y consultas de interpretación.


| Quién la probó | Qué probó | Qué pasó | Qué cambié |
|---|---|---|---|
| Profesor Lucas Fernández Aragón | Versión inicial de MIP-IA presentada en el debate del hito, 20/10/2026, todavía sin integración de IA | Confirmó el funcionamiento con datos del BCH y la claridad de la tabla de requerimientos. Recomendó ordenar las barras conforme a la tabla y sugirió que la futura integración de Gemini explicara las relaciones económicas en lenguaje llano | Se corrigió el orden de las barras y, en una fase posterior, se incorporó Gemini con instrucciones para generar interpretaciones económicas comprensibles |
| Responsable del proyecto | Exploración de proveedores directos | Se obtuvieron tablas, gráficos y coeficientes para las actividades seleccionadas | Se revisó la presentación y organización de resultados |
| Responsable del proyecto | Exploración de clientes directos | El módulo identificó actividades usuarias y sus coeficientes | Se revisaron etiquetas, gráficos y notas metodológicas |
| Responsable del proyecto | Interpretación económica con Gemini | Se generaron explicaciones en español utilizando los resultados calculados | Se ajustaron instrucciones y presentación de respuestas |
| Responsable del proyecto | Disponibilidad de modelos | Se observaron errores de disponibilidad y generación incompleta | Se incorporó un segundo modelo de interpretación |
| Responsable del proyecto | Recuperación mediante modelo alternativo | Se obtuvo una interpretación cuando el modelo principal fue configurado deliberadamente con un identificador inexistente | Se mantuvo el mecanismo de respaldo automático |
| Responsable del proyecto | Mensajes ante fallos | Se identificaron mensajes técnicos y de diagnóstico poco adecuados para usuarios finales | Se sustituyeron por advertencias comprensibles |

### Criterios de comprobación

- La matriz contiene 95 filas y 95 columnas.
- Los coeficientes utilizados son numéricos y finitos.
- Los nombres y el orden de las actividades coinciden entre filas y columnas.
- Los proveedores se identifican mediante columnas y los clientes mediante filas.
- Los coeficientes se ordenan de mayor a menor.
- Las tablas, gráficos y archivos CSV corresponden a los resultados calculados.
- Gemini interpreta resultados existentes, sin realizar los cálculos de la matriz.
- El modelo de respaldo se consulta cuando el principal no produce una respuesta válida.
- La indisponibilidad de Gemini no impide utilizar las funciones cuantitativas.
- Las credenciales privadas no se publican en el repositorio.

## Ejecutar en local

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
streamlit run app.py
```

Para habilitar las interpretaciones de Gemini, configurar `GEMINI_API_KEY` en `.streamlit/secrets.toml`, manteniendo ese archivo fuera del control de versiones.

En Streamlit Community Cloud, la clave se configura desde la administración de secretos de la aplicación.

Los módulos cuantitativos pueden utilizarse sin disponer de una clave de Gemini.

## Capturas y evidencias de la entrega

Las evidencias de funcionamiento deben incluir:

1. La aplicación publicada, mostrando sus dos módulos.
2. Un ejemplo de consulta de Proveedores directos con tabla y gráfico.
3. Un ejemplo de consulta de Clientes directos con tabla y gráfico.
4. Una interpretación económica generada mediante Gemini.
5. Una prueba del mecanismo de respaldo o de un mensaje controlado ante un fallo.
6. Una evidencia del trabajo realizado con el asistente de IA durante el desarrollo.

Las capturas no deben mostrar credenciales privadas.

## Alcance posterior al reto

HN MIP-IA forma parte de una iniciativa personal de investigación y desarrollo de herramientas de análisis económico, motivada por el interés de profundizar conocimientos en programación, inteligencia artificial y modelización de la estructura productiva de Honduras.

El proyecto constituye un ejercicio de aprendizaje, experimentación y perfeccionamiento profesional, desarrollado de manera independiente y con fines académicos.

La versión académica actual se concentra en la exploración de relaciones intersectoriales directas.

Entre las posibles ampliaciones futuras se encuentran:

- Comparación de estructuras de requerimientos directos entre dos actividades.
- Cálculo de multiplicadores de Leontief.
- Análisis de encadenamientos indirectos.
- Simulaciones de cambios en la demanda y producción.
- Integración con modelos de optimización macroeconómica.

Estas funcionalidades no forman parte de la versión actualmente implementada.

Su eventual desarrollo requerirá una evaluación metodológica específica y podrá considerar los resultados del estudio de optimización macroeconómica de Honduras.

---

**Estado de la documentación:** README actualizado para reflejar las funcionalidades implementadas, la integración de Gemini con respaldo automático y las pruebas realizadas. Permanecen pendientes la selección de prompts literales y la incorporación de evidencias definitivas de entrega.
