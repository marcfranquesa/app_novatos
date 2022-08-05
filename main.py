import streamlit as st
from source import home, game, ranking

def init():
    st.session_state.page = home
    st.session_state.home_finished = False
    st.session_state.game_finished = False

def set_config():
    st.set_page_config(page_title="FME", page_icon='📚')

def main():

    set_config()

    if "page" not in st.session_state:
        init()
    
    if st.session_state.home_finished and not st.session_state.game_finished:
        st.session_state.page = game

    if st.session_state.game_finished:
        st.session_state.page = ranking

    st.session_state.page.main()


if __name__ == "__main__":
    main()