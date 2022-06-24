import streamlit as st

st.set_page_config(
    page_title="Predicting Air Quality in Brasov",
    page_icon="🌪️️️️️",
    layout="wide"
)


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.sidebar.selectbox(
            'Menu',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
