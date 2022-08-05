import streamlit as st
import pandas as pd
import gspread
import datetime


def description():
    st.markdown(
        '''
        <h1 align="center">
            Felicitats, has arribat al final!
        </h1>

        ---

        #### Rànquing
        ''',
        unsafe_allow_html=True
    )

def exists_name(df):
    dff = df[df["Nom"] == st.session_state.user]
    return len(dff) > 0


def main():

    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sheet = gc.open_by_url(st.secrets["private_gsheets_url"]).worksheet("ranking")

    df = pd.DataFrame(sheet.get_all_records())

    description()
    
    if not exists_name(df):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        new_row = {
        "Nom": st.session_state.user,
        "Data": date,
        "Hora" : time,
        "Punts" : st.session_state.score
        }
        df = df.append(new_row, ignore_index=True)

        df = df.sort_values("Punts", ascending=False)
        df = df.reset_index(drop=True)

    st.table(df)

    sheet.update([df.columns.values.tolist()] + df.values.tolist())