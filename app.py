import streamlit as st

# Set the page title and layout as the first command
st.set_page_config(page_title="NetHandle", layout="wide")

from frontend.layout import render_layout

# Initialize session state for agent responses
if "agent_responses" not in st.session_state:
    st.session_state["agent_responses"] = {}

def main():
    # Render the main layout from the frontend module
    render_layout()

if __name__ == "__main__":
    main()
