# app libs
import streamlit as st
# data libs
import pandas as pd
# vizulization libs
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# style libs
from styles import *


class SongsDashboard:

    def __init__(self, database):
        self.database = database

    def __get_session_state(self):
        songplays_df = self.database.songplays_by_time
        songs_df = self.database.songs_by_artist
        users_df = self.database.songplays_by_user

        users_count = st.session_state.users
        users_all = st.session_state.users_all
        users_option = st.session_state.users_option

        if users_option == 'Most active users':
            users_df = users_df.sort_values(by='plays', ascending=False)
            users_label = 'most'
        else:
            users_df = users_df.sort_values(by='plays', ascending=True)
            users_label = 'least'

        if users_all:   
            users_df = users_df
            users_count = 'All'
        else:
            users_df = users_df.head(users_count)

        return {
            'songplays': songplays_df,
            'songs': songs_df,
            'users': users_df,
            'users_count': users_count,
            'users_label': users_label,
        }
    
    def __render_users_table(self, data, users, label):
        header = f"""
        <h5 style="{column_header_style}">{users} {label} active users</h5>
        <h4 style="{column_subheader_styles}">Data table</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        st.dataframe(data=data, height=280)

    def __render_word_cloud(self, data):
        header = f"""
        <h5 style="{column_header_style}">All song's titles</h5>
        <h4 style="{column_subheader_styles}">Word cloud</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        text = ' '.join(song for song in data['title'])
        wordcloud = WordCloud(background_color='white', width=380, height=280).generate(text)

        fig = plt.figure(figsize=(9, 9))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot(fig)

    def __render_plays_by_weekday(self, data):
        header = f"""
        <h5 style="{column_header_style}">All songplays</h5>
        <h4 style="{column_subheader_styles}">By Weekdays</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        data = data.groupby(by=['weekday'], as_index=False).aggregate(
            {'timestamp': 'count'})

        weekdays = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']

        graph = alt.Chart(data).mark_bar().encode(
            x=alt.X('weekday:N', sort=weekdays),
            y=alt.Y('timestamp:Q', title='plays'),
            color=alt.Color('weekday:N', sort=weekdays, legend=None,
                            scale=alt.Scale(scheme='teals'))
        ).properties(
            width='container',
            height=300
        ).interactive()

        st.altair_chart(graph, use_container_width=True)

    def __render_plays_by_month(self, data):
        header = f"""
        <h5 style="{column_header_style}">All songplays</h5>
        <h4 style="{column_subheader_styles}">By Weekdays</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        data = data.groupby(by=['hour'], as_index=False).aggregate(
            {'timestamp': 'count'})

        graph = alt.Chart(data).mark_bar().encode(
            x=alt.X('hour:Q'),
            y=alt.Y('timestamp:Q', title='plays'),
            color=alt.Color('hour:Q', sort='x', legend=None,
                            scale=alt.Scale(scheme='tealblues'))
        ).properties(
            width='container',
            height=300
        ).interactive()

        st.altair_chart(graph, use_container_width=True)

    def render(self):
        session_state = self.__get_session_state()

        songplays = session_state['songplays']
        songs = session_state['songs']
        users = session_state['users']
        users_count = session_state['users_count']
        users_label = session_state['users_label']

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            self.__render_users_table(users, users_count, users_label)

        with col2:
            self.__render_plays_by_weekday(songplays)

        with col3:
            self.__render_plays_by_month(songplays)
        
        with col4:
            self.__render_word_cloud(songs)
