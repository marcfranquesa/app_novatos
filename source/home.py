import streamlit as st
import gspread
import pandas as pd

def description():
    st.markdown(
        '''
        <h1 align="center">
            Benvinguts a l'endevinador de matemàtics 👋
        </h1>

        ---

        #### Informació
        
        Per fi teniu les descripcions dels de segón!
        Hem decidit fer un petit joc en el que haureu
        d'ajuntar el matemàtic amb la seva descripció.
        
        Funcionament:
        1. Si encerteu guanyeu un punt
        2. Si falleu perdeu un punt
        
        Ben senzill oi? Tenim un rànquing i el 
        guanyador s'endurà premi! Per començar
        introdueix el teu nom i prem enter.
        ''',
        unsafe_allow_html=True
    )

def text_input():
    name = st.text_input("Nom:")
    return name


def finished():
    st.session_state.home_finished = True

def exists(user):
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sheet = gc.open_by_url(st.secrets["private_gsheets_url"]).worksheet("ranking")
    df = pd.DataFrame(sheet.get_all_records())
    dff = df[df["Nom"] == user]
    return len(dff) > 0

def main():
    description()
    user = text_input()
    if user != '':
        st.session_state.user = user

    if "user" in st.session_state and exists(st.session_state.user):
        st.error("Aquest nom ja s'està utilitzant!")

    elif "user" in st.session_state:
        col1, col2 = st.columns(2)
        col1.write(f"Ets el/la {st.session_state.user}?")
        col2.button(
            "Si", 
            on_click=finished, 
        )
    