# app libs
import streamlit as st
# data libs
import pandas as pd
# vizulization libs
import altair as alt
# sql queries
from queries import songplays_by_user


class User:

    def __init__(self, connection):
        self.connection = connection
    
    def __init_state(self):
        if 'users' not in st.session_state:
            st.session_state.users = 10

    def __get_dataframe(self):
        return pd.read_sql(songplays_by_user, self.connection)
        
    def render(self):
        users = st.session_state.users
        users_option = st.session_state.users_option

        if users_option == 'Most active users':
            users_df = self.__get_dataframe().sort_values(by='plays', ascending=False)
            users_option_label = 'most'
            graph_sort = '-x'
        else:
            users_df = self.__get_dataframe().sort_values(by='plays', ascending=True)
            users_option_label = 'least'
            graph_sort = 'x'

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write(f"""
            ##### {users} {users_option_label} active users by songs played
            """)

            graph = alt.Chart(users_df.head(users)) \
                .mark_bar().encode(
                    x='plays',
                    y=alt.Y('user:N', sort=graph_sort)
            ).properties(
                width='container',
                height=300
            ).interactive()

            st.altair_chart(graph, use_container_width=True)
        
        with col2:
            st.write(f"""
            ##### {users} {users_option_label} active users by gender
            """)

            graph = alt.Chart(users_df.head(users)).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="gender", type="nominal", aggregate="count"),
                color=alt.Color(field="gender", type="nominal"),
            ).properties(
                width='container',
                height=300
            ).interactive()

            st.altair_chart(graph, use_container_width=True)
        
        with col3:
            st.write(f"""
            ##### {users} {users_option_label} active users by subscription
            """)

            graph = alt.Chart(users_df.head(users)).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="level", type="nominal", aggregate="count"),
                color=alt.Color(field="level", type="nominal"),
            ).properties(
                width='container',
                height=300
            ).interactive()

            st.altair_chart(graph, use_container_width=True)
        
        with col4:
            st.write(f"""
            ##### {users} {users_option_label} active users table
            """)
            
            st.dataframe(data=users_df.head(users), height=280)
