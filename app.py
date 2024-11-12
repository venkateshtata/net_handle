import streamlit as st
from frontend.layout import render_layout

# Set the page title and layout
st.set_page_config(page_title="NetHandle", layout="wide")

def main():
    # Render the main layout from the frontend module
    render_layout()

if __name__ == "__main__":
    main()
