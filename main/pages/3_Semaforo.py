import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Función para calcular la fecha de finalización de cada actividad
def calcular_fecha_fin(fecha_inicio, duracion):
    fecha_fin = fecha_inicio + timedelta(days=duracion)
    return fecha_fin

# Función para generar el semáforo de actividades
def generar_semaforo(actividades, fecha_actual):
    semaforo = ""
    for actividad in actividades:
        fecha_fin_actividad = calcular_fecha_fin(actividad["fecha_inicio"], actividad["duracion"])
        if fecha_actual < actividad["fecha_inicio"]:
            semaforo += f"⚪️ {actividad['nombre']} - No iniciada\n"
        elif fecha_actual <= fecha_fin_actividad:
            semaforo += f"🟡 {actividad['nombre']} - En progreso\n"
        else:
            semaforo += f"🟢 {actividad['nombre']} - Completada\n"
    return semaforo

# Título de la aplicación
st.title("Gestor de Proyectos tipo Microsoft Project")

# Preguntas al usuario
fecha_inicio_proyecto = st.date_input("1. Fecha de inicio del proyecto", datetime.now())
num_actividades = st.number_input("Número de actividades a realizar", min_value=1, value=1, step=1)

# Crear lista de actividades con sus detalles
lista_actividades = []
for i in range(num_actividades):
    st.sidebar.subheader(f"Actividad {i + 1}")
    nombre_actividad = st.sidebar.text_input(f"Nombre de la actividad {i + 1}")
    duracion_actividad = st.sidebar.number_input(f"Duración de la actividad {i + 1} (en días)", min_value=1, value=1, step=1)

    actividad = {
        "nombre": nombre_actividad,
        "fecha_inicio": fecha_inicio_proyecto,
        "duracion": duracion_actividad
    }

    lista_actividades.append(actividad)

# Función para verificar dependencias y establecer fechas de inicio
def establecer_fechas_inicio(actividades):
    for i in range(1, len(actividades)):
        dependencia = st.selectbox(f"Dependencia de inicio para '{actividades[i]['nombre']}':", [act['nombre'] for act in actividades[:i]])
        dependencia_idx = next((idx for idx, act in enumerate(actividades[:i]) if act['nombre'] == dependencia), None)
        
        if dependencia_idx is not None:
            actividades[i]['fecha_inicio'] = calcular_fecha_fin(actividades[dependencia_idx]['fecha_inicio'], actividades[dependencia_idx]['duracion'])
        else:
            st.warning(f"No se encontró la dependencia '{dependencia}', se establecerá la fecha de inicio predeterminada.")



# Establecer fechas de inicio según dependencias
establecer_fechas_inicio(lista_actividades)

# Generar y mostrar el semáforo de actividades
semaforo = generar_semaforo(lista_actividades, datetime.now())
st.subheader("Semáforo de Actividades")
st.text(semaforo)

# Botón para iniciar el proyecto
if st.button("Iniciar Proyecto"):
    st.success("¡Proyecto iniciado!")

# Generar y mostrar el diagrama de Gantt
fig = px.timeline(lista_actividades, x_start='fecha_inicio', x_end=px.data.gapminder()['pop'], y='nombre')
fig.update_yaxes(categoryorder='total ascending')
fig.update_layout(xaxis_title='Fecha de inicio', yaxis_title='Actividades', title='Diagrama de Gantt')
st.plotly_chart(fig)