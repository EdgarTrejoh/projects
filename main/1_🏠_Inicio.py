import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(
     page_title="Inicio", 
     page_icon="📈"
     )

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

"-------------------------------------------"

#Conecciones
conn = st.connection("gsheets", type=GSheetsConnection)

refinanciamiento = conn.read(worksheet="Refinanciamiento", usecols=list(range(4)), ttl=5)
refinanciamiento = refinanciamiento.dropna(how="all")
pie_casa = conn.read(worksheet="PieCasa", usecols=list(range(4)), ttl=5)
pie_casa = pie_casa.dropna(how="all")

#Layout de Refinanciamiento 
estatus_refinanciamiento = refinanciamiento.groupby(["Estatus"]).count()
f_inicio_r = (refinanciamiento['FechaInicio'].min())
f_inicio_r = pd.to_datetime(f_inicio_r)
f_inicio_r = f_inicio_r.strftime('%d-%m-%Y')
f_fin_r = refinanciamiento['FechaFin'].max()
f_fin_r = pd.to_datetime(f_fin_r)
f_fin_r = f_fin_r.strftime('%d-%m-%Y')

#Layout de Pie de Casa
estatus_pie_Casa = pie_casa.groupby(["Estatus"]).count()
f_inicio_pC = (pie_casa['FechaInicio'].min())
f_fin_pC = pie_casa['FechaFin'].max()

st.markdown("## Estatus de los proyectos asignados")

refinanc, piecasa = st.tabs([":date: Refinanciamiento", 
                            ":clipboard: Pie de Casa", 
                            ])


#Layout de pestañas
with refinanc:
    
    st.markdown(f"#### :blue[Fecha de inicio {f_inicio_r}]")

    st.markdown(f"#### :blue[Fecha fin {f_fin_r}]")

#Vista de project Refinanciamiento:
    
    project_ref = px.timeline(
        refinanciamiento,
        x_start ='FechaInicio',
        x_end = 'FechaFin',
        y = 'Actividad',
        color ='Actividad',
        color_discrete_sequence =px.colors.sequential.Plasma_r,
        labels = {'Actividad': 'Actividad'},
        title = "Cronograma de actividades"
    )

    project_ref.update_yaxes(autorange="reversed")

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    project_ref.add_shape(
        type= 'line',
        x0 = fecha_actual,
        x1 = fecha_actual,
        y0 = 0,
        y1 = 1,
        xref = 'x',
        yref = 'paper', # yref='paper' para que sea en relación a la altura del gráfico
        line = dict(color='red', width=2), # Personalizar el color y el ancho de la línea
    )

    project_ref.update_layout(
        height = 380,
        width=480,
        showlegend = False,
        title_font=dict(
            color="#027034",
            size=20
            )
        )

    st.plotly_chart(project_ref, use_container_width=True)

    # Gráfico con conteo de actividad por estatus

    refinanciaminto_status = px.bar(
        estatus_refinanciamiento, 
        x =estatus_refinanciamiento.index,
        y = "Actividad",
        title = "Resumen de Actividades",
    )

    refinanciaminto_status.update_xaxes(title_text="Estatus")

    refinanciaminto_status.update_yaxes(
        title_text="Actividades (No.)")

    refinanciaminto_status.update_layout(
        height = 380,
        width=480,
        showlegend = False,
        title_font=dict(
            color="#027034",
            size=20
            )
        )

    st.plotly_chart(refinanciaminto_status, use_container_width=True)

with piecasa:

    st.markdown(f"#### :blue[Fecha de inicio {f_inicio_pC}]")

    st.markdown(f"#### :blue[Fecha fin {f_fin_pC}]")

    pie_casa_status = px.bar(
        estatus_pie_Casa, 
        x =estatus_pie_Casa.index,
        y = "Actividad",
        title = "Resumen",
    )

    pie_casa_status.update_xaxes(title_text="Estatus")

    pie_casa_status.update_yaxes(
            title_text="Actividades (No.)")

    pie_casa_status.update_layout(
            height = 380,
            width=480,
            showlegend = False,
            title_font=dict(
                color="#027034",
                size=20
                )
            )

    st.plotly_chart(pie_casa_status, use_container_width=True)

