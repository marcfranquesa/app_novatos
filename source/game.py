import random
from typing import List

import streamlit as st
import yaml

from source import utils


def get_main_name() -> str:
    name = st.session_state.names[st.session_state.position]
    st.session_state.position += 1
    return name


def get_9_names() -> List[str]:
    names = [st.session_state.name]
    while len(names) < 9:
        name = random.choice(st.session_state.names)
        if name not in names:
            names.append(name)
    random.shuffle(names)
    return names


def init(post_init: bool = False):
    if not post_init:
        with open(r"resources/descriptions.yaml") as file:
            st.session_state.descriptions = yaml.load(file, Loader=yaml.FullLoader)
        st.session_state.names = list(st.session_state.descriptions.keys())
        random.shuffle(st.session_state.names)
        st.session_state.position = 0
        st.session_state.score = 0

    st.session_state.name = get_main_name()
    st.session_state.names_to_show = get_9_names()


def restart():
    if st.session_state.position == len(st.session_state.names):
            st.session_state.game_finished = True
    else:
        init(post_init=True)


def check(selected: str, skipped: bool = False):
    if skipped:
        st.session_state.pop("guess", None)
    elif selected == st.session_state.name:
        st.session_state.score += 3
        st.session_state.guess = True
    else:
        st.session_state.guess = False
        st.session_state.score -= 1
    restart()


def show_guess():
    if "guess" in st.session_state:
        previous = utils.beautify_name(
            st.session_state.names[st.session_state.position - 2]
        )
        if st.session_state.guess:
            st.success(f"Has encertat l'anterior 😊! Era el/la {previous}.")
        else:
            st.error(f"Has fallat l'anterior ☹️! Era el/la {previous}.")

def show_main():
    st.subheader("Descripció:")
    st.markdown(
        f"""
        <div style="
            background: ghostwhite; 
            font-size: 20px; 
            padding: 15px; 
            border: 1px solid lightgray; 
            margin: 20px;
            text-align: center;
            color: pink;">
        {st.session_state.descriptions[st.session_state.name]}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write('')


def show_option(position, location):
    name = st.session_state.names_to_show[position]
    location.image(
        utils.get_image(
            name
        ),
        width=200,
    )
    location.button(
        utils.beautify_name(name), 
        on_click=check, 
        args=[st.session_state.names_to_show[position]]
    )


def show_options():
    st.subheader("Opcions:")
    for i in range(3):
        col1, col2, col3 = st.columns(3)
        show_option(3 * i, col1)
        show_option(3 * i + 1, col2)
        show_option(3 * i + 2, col3)
        

def main():
    st.write(
        """
        # Endevina el matemàtic
        """
    )

    if "names" not in st.session_state:
        init()

    reset, win, _ = st.columns([0.7, 1, 1])
    reset.button("Saltar matemàtic", on_click=check, args=[None, True])

    show_guess()
    show_main()
    show_options()
    
    win.button(f"🏆 {st.session_state.score}")
