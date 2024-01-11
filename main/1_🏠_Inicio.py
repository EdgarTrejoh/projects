import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots
from streamlit_gsheets import GSheetsConnection

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

#Conection
conn = st.connection("gsheets", type=GSheetsConnection)

refinanciamiento = conn.read(worksheet="Refinanciamiento", usecols=list(range(4)), ttl=5)
refinanciamiento = refinanciamiento.dropna(how="all")

pie_casa = conn.read(worksheet="PieCasa", usecols=list(range(4)), ttl=5)
pie_casa = pie_casa.dropna(how="all")

estatus_refinanciamiento = refinanciamiento.groupby(["Estatus"]).count()
estatus_pie_Casa = pie_casa.groupby(["Estatus"]).count()


st.write("Estatus de los proyectos asignados")


refinanc, piecasa = st.tabs([":date: Refinanciamiento", 
                            ":clipboard: Pie de Casa", 
                            ])

with refinanc:
    
    refinanciaminto_status = px.bar(
        estatus_refinanciamiento, 
        x =estatus_refinanciamiento.index,
        y = "Actividad",
        title = "Resumen",
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

