import streamlit as st
from st_paywall import add_auth
from streamlit_option_menu import option_menu

st.set_page_config(
     page_title="Home", 
     page_icon=":house_with_garden:"
     )

st.markdown("# :turtle: Suscribete :turtle: ")

selected = option_menu(
        menu_title='Main Menú',
        options = ["Home","Projects", "Contact"],
        icons =["house", "book", "envelope"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal",
        styles = {
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color":"orage", "font-size": "25px"},
            "nav-link": {
                "font-size": "25px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee"
            },
            "nav-link-selected":{"backgroind-color": "green"},
        }
    )



if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Projects":
    st.title(f"You have selected {selected}")
if selected == "Contact":
    st.title(f"You have selected {selected}")


add_auth(required=True)

st.write(f"Suscription status : {st.session_state.user_subscribed}")
st.write("You´re all set and subscribed insert--emoji")
st.write(f"The email registered is {st.session_state.email}")

with st.sidebar:
    selected = option_menu(
        menu_title='Main Memnú',
        options = ["Home","Projects", "Contact"]
    )

if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Projects":
    st.title(f"You have selected {selected}")
if selected == "Contact":
    st.title(f"You have selected {selected}")