import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configure
st.set_page_config(
     page_title="Gerencia Sr. Innovación & Diseño", 
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

projects = conn.read(worksheet="Refinanciamiento", usecols=list(range(10)), ttl=5)

existing_data = conn.read(worksheet="Refinanciamiento", usecols=list(range(10)), ttl=5)
existing_data = existing_data.dropna(how="all")

# Constants
Estatus = [
        "No Aplica",
        "En Proceso",
        "Finalizado",
        "Suspensión Temporal",
]

Actividades = conn.read(worksheet="Actividades", usecols=list(range(1)), ttl=5)
Actividades = Actividades.dropna(how="all")
Actividades_sorted = sorted(Actividades)

st.dataframe(Actividades_sorted)

st.markdown("# :blue[Seguimiento de proyectos :chart_with_upwards_trend:]")
#st.info(
#    "Selecciona una acción",
#    icon="ℹ️",
#)

action = st.selectbox(
    "Elige una acción:",
    [
        "Ver Proyecto",
        "Agregar actividades al proyecto",
        "Actualizar proyecto",
     ]
)

if action == "Agregar actividades al proyecto":
    st.markdown("## :green[Ingresa las actividades del proyecto :notebook:]")
    with st.form(key="project_form"):
        actividad = st.selectbox(
            "Actividad*", options=Actividades_sorted, index=None
          )
        estatus = st.selectbox(
            "Estatus*", options=Estatus, index=None
        )
        inicio = st.date_input(label="Fecha de inicio")
        fin = st.date_input(label="Fecha fin")
        comentarios = st.text_area(label="Comentarios")
        st.markdown("**Obligatorios*")
        submit_button = st.form_submit_button(label="Agregar actividad al proyecto")

        if submit_button:
            if not actividad or not estatus:
                st.warning("Faltan campos obligatorios")
            elif existing_data["Actividad"].str.contains(actividad).any():
                st.warning("La actividad ya existe, selecciona la opción Actualizar proyecto")
            elif fin < inicio:
                st.warning("Fecha fin no puede ser menor a la fecha inicio")
            else:
                actividad_data = pd.DataFrame(
                    [
                        {
                            "Actividad": actividad,
                            "Estatus": estatus,
                            "FechaInicio": inicio.strftime("%Y-%m-%d"),
                            "FechaFin": fin.strftime("%Y-%m-%d"),
                            "Comentarios": comentarios,
                        }
                    ]
                )
                updated_df = pd.concat([existing_data, actividad_data], ignore_index=True)
                conn.update(worksheet="Refinanciamiento", data=updated_df)
                st.success("Actividad creada con éxito!")

elif action == "Actualizar proyecto":
    st.markdown("Selecciona la actividad a actualizar.")

    update = st.selectbox(
        "Selecciona la actividad", options=existing_data["Actividad"].tolist()
    )
    actividad_data = existing_data[existing_data["Actividad"] == update].iloc[
        0
    ]

    with st.form(key="update_form"):
        actividad = st.text_input(
            "Actividad*", value=actividad_data["Actividad"]
            
          )
        estatus = st.selectbox(
            "Estatus**", 
            options=Estatus, 
            index=Estatus.index(actividad_data["Estatus"]),
        )
        inicio = st.date_input(
            label="Fecha de inicio", value=pd.to_datetime(actividad_data["FechaInicio"])
        )
        fin = st.date_input(
            label="Fecha fin",value=pd.to_datetime(actividad_data["FechaFin"])
        )   
        comentarios = st.text_area(
            label="Comentarios", value=actividad_data["Comentarios"]
        )
           
        st.markdown("**No actualizar*")
        st.markdown("***Requerido*")
        update_button = st.form_submit_button(label="Actualizar actividad del proyecto")

        if update_button:
            if not Estatus:
                st.warning("Capturar campos obligatorios.")
            else:
                # Removing old entry
                existing_data.drop(
                    existing_data[
                        existing_data["Actividad"] == update
                    ].index,
                    inplace=True,
                )
                # Creating updated data entry
                updated_project = pd.DataFrame(
                    [
                        {
                            "Actividad": actividad,
                            "Estatus": estatus,
                            "FechaInicio": inicio.strftime("%Y-%m-%d"),
                            "FechaFin": fin.strftime("%Y-%m-%d"),
                            "Comentarios": comentarios,
                        }
                    ]
                )
                # Adding updated data to the dataframe
                updated_df = pd.concat(
                    [existing_data, updated_project], ignore_index=True
                )
                conn.update(worksheet="Refinanciamiento", data=updated_df)
                st.success("Actividad actualizada con éxito!")

elif action == "Ver Proyecto":
    projects = projects.dropna(how="all")    
    st.dataframe(projects, hide_index=True)