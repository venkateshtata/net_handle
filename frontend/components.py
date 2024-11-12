# frontend/components.py

import streamlit as st

def render_search_bar():
    # Create a search bar input field
    search_query = st.text_input("Search Agents", placeholder="Type here to search...")
    # Display search results or feedback (optional)
    if search_query:
        st.write(f"Searching for: {search_query}")

def render_sidebar():
    # Sidebar title
    st.sidebar.markdown("<h2 style='color: white;'>Menu</h2>", unsafe_allow_html=True)

    # Sidebar buttons with divider lines and custom CSS for symmetry
    st.sidebar.markdown(
        """
        <style>
        .sidebar-button {
            border: none;
            padding: 10px 20px;
            width: 100%;
            background-color: #333333;
            color: white;
            font-size: 16px;
            text-align: left;
            cursor: pointer;
            margin: 0;
        }
        .sidebar-button:hover {
            background-color: #444444;
        }
        </style>
        
        <button class="sidebar-button">Home</button>
        <button class="sidebar-button">My Handlers</button>
        <button class="sidebar-button">Profile Settings</button>
        """,
        unsafe_allow_html=True
    )
