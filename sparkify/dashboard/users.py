# app libs
import streamlit as st
# vizulization libs
import altair as alt
import pydeck as pdk
# style libs
from styles import *


class UsersDahsboard:

    def __init__(self, database):
        self.database = database

    def __get_session_state(self):
        locations_df = self.database.artists_by_location
        users_df = self.database.songplays_by_user

        users_count = st.session_state.users
        users_all = st.session_state.users_all
        users_option = st.session_state.users_option

        if users_option == 'Most active users':
            users_df = users_df.sort_values(by='plays', ascending=False)
            users_label = 'most'
            users_sort = '-x'
        else:
            users_df = users_df.sort_values(by='plays', ascending=True)
            users_label = 'least'
            users_sort = 'x'

        if users_all:   
            users_df = users_df
            users_count = 'All'
        else:
            users_df = users_df.head(users_count)

        return {
            'locations': locations_df,
            'users': users_df,
            'users_count': users_count,
            'users_label': users_label,
            'users_sort': users_sort
        }

    def __render_songplays_chart(self, data, users, label, sort):
        header = f"""
        <h5 style="{column_header_style}">{users} {label} active users</h5>
        <h4 style="{column_subheader_styles}">By songs played</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        graph = alt.Chart(data).mark_bar().encode(
            x='plays',
            y=alt.Y('user:N', sort=sort),
            color=alt.Color('user:N', sort=sort, legend=None,
                            scale=alt.Scale(scheme='teals'))
        ).properties(
            width='container',
            height=300
        ).interactive()

        st.altair_chart(graph, use_container_width=True)

    def __render_gender_chart(self, data, users, label):
        header = f"""
        <h5 style="{column_header_style}">{users} {label} active users</h5>
        <h4 style="{column_subheader_styles}">By gender</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        graph = alt.Chart(data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field='gender', type='nominal', aggregate='count'),
            color=alt.Color(field='gender', type='nominal', scale=alt.Scale(scheme='blues')),
        ).properties(
            width='container',
            height=300
        ).interactive()

        st.altair_chart(graph, use_container_width=True)

    def __render_subscription_chart(self, data, users, label):
        header = f"""
        <h5 style="{column_header_style}">{users} {label} active users</h5>
        <h4 style="{column_subheader_styles}">By subscription</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        graph = alt.Chart(data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field='level', type='nominal',
                            aggregate='count'),
            color=alt.Color(field='level', type='nominal',
                            scale=alt.Scale(scheme='tealblues')),
        ).properties(
            width='container',
            height=300
        ).interactive()

        st.altair_chart(graph, use_container_width=True)
    
    def __render_artists_by_location(self, data):
        header = f"""
        <h5 style="{column_header_style}">All artists</h5>
        <h4 style="{column_subheader_styles}">Location coordinates</h4>
        """
        st.markdown(header, unsafe_allow_html=True)

        data = data.loc[data['latitude'].notnull() &
                        data['longitude'].notnull()]

        latitude = data['latitude'].mean()
        longitude = data['longitude'].mean()

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=1,
                height=280,
                width=370
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data,
                    get_position=['longitude', 'latitude'],
                    get_color='[30, 150, 200, 160]',
                    radius_scale=2,
                    radius_min_pixels=8,
                    radius_max_pixels=128,
                    line_width_min_pixels=1,
                    get_radius="exits_radius",
                    auto_highlight=True
                ),
            ],
        ))

    def render(self):
        session_state = self.__get_session_state()

        users = session_state['users']
        locations = session_state['locations']
        users_count = session_state['users_count']
        users_label = session_state['users_label']
        users_sort = session_state['users_sort']

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            self.__render_songplays_chart(
                users, users_count, users_label, users_sort)

        with col2:
            self.__render_gender_chart(users, users_count, users_label)

        with col3:
            self.__render_subscription_chart(
                users, users_count, users_label)

        with col4:
            self.__render_artists_by_location(locations)
