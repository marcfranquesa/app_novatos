import PIL
import random
import streamlit as st
import yaml


def get_name():
    name = st.session_state.names[st.session_state.position]
    st.session_state.position += 1
    return name

def get_image():
    return PIL.Image.open(f"resources/images/{st.session_state.name}.jpg")

def get_9_descriptions():
    descriptions = [st.session_state.descriptions[st.session_state.name]]
    while len(descriptions) < 9:
        description = random.choice(list(st.session_state.descriptions.values()))
        if description not in descriptions:
            descriptions.append(description)
    random.shuffle(descriptions)
    return descriptions


def init(post_init=False):
    if not post_init:
        with open(r"resources/descriptions.yaml") as file:
            st.session_state.descriptions = yaml.load(file, Loader=yaml.FullLoader)
        st.session_state.names = list(st.session_state.descriptions.keys())
        random.shuffle(st.session_state.names)
        st.session_state.position = 0
        st.session_state.score = 0

    st.session_state.name = get_name()
    st.session_state.image = get_image()
    st.session_state.descriptions_to_show = get_9_descriptions()


def restart():
    if st.session_state.position == len(st.session_state.names):
            st.session_state.game_finished = True
    else:
        init(post_init=True)

def check(description):
    if description == st.session_state.descriptions[st.session_state.name]:
        st.session_state.score += 1
        restart()
    else:
        st.session_state.score -= 1

def show_descriptions():
    for i in range(3):
        desc1, desc2, desc3 = st.columns(3)
        desc1.button(
            st.session_state.descriptions_to_show[3 * i], 
            on_click=check, 
            args=[st.session_state.descriptions_to_show[3 * i]]
        )
        desc2.button(
            st.session_state.descriptions_to_show[3 * i + 1],
            on_click=check,
            args=[st.session_state.descriptions_to_show[3 * i + 1]]
        )
        desc3.button(
            st.session_state.descriptions_to_show[3 * i + 2],
            on_click=check, 
            args=[st.session_state.descriptions_to_show[3 * i + 2]]
        )

def main():
    st.write(
        """
        # Endevina el matemàtic
        """
    )

    if "names" not in st.session_state:
        init()

    reset, win, _ = st.columns([0.5, 1, 1])
    reset.button("Nou matemàtic", on_click=restart)

    _, image, _ = st.columns(3)
    image.image(st.session_state.image, width=200)
    
    show_descriptions()
    
    win.button(f"🏆 {st.session_state.score}")


if __name__ == '__main__':
    main()
