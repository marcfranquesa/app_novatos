import streamlit as st

from source import utils


def description():
    st.markdown(
        """
        <h1 align="center">
            Felicitats, has arribat al final!
        </h1>

        ---

        #### Rànquing
        """,
        unsafe_allow_html=True
    )


def ranking():
    sheet = utils.get_sheet()
    df = utils.get_ranking(sheet=sheet)
    
    if not utils.exists_user(
        st.session_state.user,
        df,
        sheet=sheet
    ):
        row = {
            "Nom": st.session_state.user,
            "Data": utils.get_date(),
            "Hora" : utils.get_time(),
            "Punts" : st.session_state.score
        }
        df = utils.write_new_row(row, df, sheet)

    st.table(df)


def main():
    description()
    ranking()

    

    