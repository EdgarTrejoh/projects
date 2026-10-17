# projects

## Propósito identificado
Repositorio con código para un prototipo de gestión y seguimiento de actividades mediante Streamlit.

## Módulo inspeccionado
`main/pages/3_Semaforo.py` incluye:
- Captura de actividades y duración.
- Cálculo de fechas estimadas.
- Dependencias secuenciales.
- Clasificación visual de actividades tipo semáforo.
- Intento de visualización de cronograma con Plotly.

## Estado
**Clasificación propuesta:** PROTOTIPO / REVISIÓN TÉCNICA.
No se considera que sea un repositorio genérico vacío: contiene código específico de gestión de proyectos.

## Advertencias técnicas
El código inspeccionado construye un gráfico con una columna para `x_end` que no corresponde a las fechas calculadas de las actividades. Se debe probar y corregir antes de declarar funcional esa visualización.
Los estados del semáforo también deben revisarse contra sus reglas temporales de negocio.

## Pendientes de decisión
- [ ] Determinar si la herramienta conserva utilidad independiente.
- [ ] Verificar el árbol completo y el punto de arranque.
- [ ] Probar el módulo y corregir errores identificados.
- [ ] Decidir mantener, documentar como experimento o congelar.
- [ ] Identificar posibles integraciones sólo con una decisión formal.

## Evidencia
- Módulo revisado: https://github.com/EdgarTrejoh/projects/blob/main/main/pages/3_Semaforo.py
