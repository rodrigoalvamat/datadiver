# system libs
import sys
from database import Database
# app libs
import streamlit as st
# style libs
from styles import *
# UI component libs
from sidebar import Sidebar
from songs import SongsDashboard
from users import UsersDahsboard


class App:

    def __init__(self, cloud):
        self.database = Database(cloud)
        self.__config_page()

    def __config_page(self):
        st.set_page_config(
            page_title="DataDiver - Sparkify Dashboard",
            page_icon="images/favicon.ico",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get help': 'https://www.linkedin.com/in/rodrigo-alvarenga-mattos',
                'Report a bug': "https://github.com/rodrigoalvamat/portfolio/issues",
                'About': "# This is a Data Enginner ETL Pipeline showcase app!"
            }
        )


    def render(self):
        header = f"""
        <header style="{page_header_style}">Sparkify Dashboard</header>
        """
        st.markdown(header, unsafe_allow_html=True)

        sidebar = Sidebar(200)
        sidebar.render()

        users = UsersDahsboard(self.database)
        users.render()

        songs = SongsDashboard(self.database)
        songs.render()


if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == 'cloud':
        app = App(cloud=True)
    else:
        app = App(cloud=False)

    app.render()
