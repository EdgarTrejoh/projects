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
st.title("Gestor de Proyectos")

# Preguntas al usuario
fecha_inicio_proyecto = st.date_input("1. Fecha de inicio del proyecto", datetime.now())
actividades = st.text_area("2. Actividades a realizar (una por línea)").split("\n")
duracion_actividades = st.text_area("3. Duración de cada actividad (en días, una por línea)").split("\n")

# Crear lista de actividades con sus detalles
lista_actividades = []
for nombre, duracion_str in zip(actividades, duracion_actividades):
    if nombre and duracion_str:
        duracion = int(duracion_str)
        actividad = {
            "nombre": nombre,
            "fecha_inicio": fecha_inicio_proyecto,
            "duracion": duracion
        }
        lista_actividades.append(actividad)

# Generar y mostrar el semáforo
semaforo = generar_semaforo(lista_actividades, datetime.now())
st.subheader("Semáforo de Actividades")
st.text(semaforo)

# Generar y mostrar el diagrama de Gantt
fig = px.timeline(lista_actividades, x_start='fecha_inicio', x_end=px.data.gapminder()['pop'], y='nombre')
fig.update_yaxes(categoryorder='total ascending')
fig.update_layout(xaxis_title='Fecha de inicio', yaxis_title='Actividades', title='Diagrama de Gantt')
st.plotly_chart(fig)