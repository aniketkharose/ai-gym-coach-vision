import streamlit as st
from services.persistence.exercise_repository import get_or_create_user
from services.ui import components as ui


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    ui.login_hero()

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Name (unique)",
            placeholder="unique name e.g. aniket"
        )

        submit_button = st.form_submit_button(
            "START SESSION",
            width="stretch",
            key="login_submit"
        )

    if submit_button:
        username = (username or "").strip()

        if not username:
            st.error("Name cannot be empty. Please enter a valid name.")
            return False

        user = get_or_create_user(username)
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]

        st.rerun()

    return False