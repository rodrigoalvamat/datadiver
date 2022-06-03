# app libs
import streamlit as st


class Sidebar:

    def __init__(self, size):
        self.size = size

    def render(self):
        with st.sidebar:
            user_option = st.selectbox(
                'How would you like to sort users?',
                ('Most active users', 'Least active users'), key='users_option')
            user_slider = st.slider('Number of users', min_value=5,
                                  max_value=20, value=10, step=5, key='users')
