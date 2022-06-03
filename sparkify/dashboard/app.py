# system libs
import sys
# app libs
import streamlit as st
# sql libs
from sqlalchemy import create_engine
# UI component libs
from sidebar import Sidebar
from users import User


class App:

    def __init__(self, cloud):
        self.connection = self.__create_connection(cloud)
        self.__config_page()

    def __create_connection(self, cloud):
        if cloud:
            username = 'erxsjqjd'
            password = 'OhDRrRbv8b59vECc08ENtqtG3rFekShP'
            host = 'heffalump.db.elephantsql.com'
            database = username
            dbconf = f'postgresql+psycopg2://{username}:{password}@{host}/{database}'
        else:
            dbconf = 'postgresql+psycopg2://student:student@127.0.0.1/sparkifydb'

        return create_engine(dbconf)

    def __config_page(self):
        st.set_page_config(
            page_title="Sparkify Dashboard",
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
        sidebar = Sidebar(200)
        sidebar.render()

        st.write("""
        # Sparkify Dashboard
        """)

        user = User(self.connection)
        user.render()


if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == 'cloud':
        app = App(cloud=True)
    else:
        app = App(cloud=False)

    app.render()
