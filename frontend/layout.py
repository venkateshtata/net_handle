import streamlit as st
from frontend.components import render_search_bar, render_sidebar

def render_layout():
    # Render the header
    st.markdown("<h1 style='text-align: center;'>NetHandle</h1>", unsafe_allow_html=True)

    # Render the sidebar
    render_sidebar()

    # Render the search bar
    render_search_bar()
    
    # Placeholder for displaying content
    st.write("Use the search bar above to search from hundreds of available handlers for your task!")
