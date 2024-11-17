import streamlit as st
from backend.agent_manager import AgentManager
from frontend.components import render_search_bar, render_sidebar

agent_manager = AgentManager()

def render_layout():
    # Header
    st.markdown("<h1 style='text-align: center; color: #333333;'>NetHandle</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555555;'>AI Agent Platform</h4>", unsafe_allow_html=True)
    
    render_sidebar()
    
    # Render main content based on page
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        render_home_page()
    elif st.session_state.page == "My Handlers":
        render_my_handlers()
    elif st.session_state.page == "ShoppingHandler":
        render_agent_search_page("ShoppingHandler")

    # Footer
    st.markdown("<hr style='border:1px solid #DDDDDD;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #AAAAAA;'>NetHandle Platform - Version 1.0 | © 2024</p>",
        unsafe_allow_html=True
    )


def render_home_page():
    st.title("Welcome to NetHandle")
    st.write("Explore and interact with various AI agents for different tasks.")
    st.markdown("<hr>", unsafe_allow_html=True)
    render_search_bar()  # Search for available agents

def render_agent_search_page(agent_name):
    agent = agent_manager.get_agent(agent_name)
    if agent:
        st.subheader(f"{agent_name} Search")
        query = st.text_input(f"Search with {agent_name}", placeholder="Type your query here...")

        if query:
            results = agent.search(query)  # Expected to be a list of dictionaries

            # Check if results are valid
            if not isinstance(results, list) or not all(isinstance(item, dict) for item in results):
                st.error("Error: Expected search results as a list of dictionaries.")
                return
            if not results:
                st.write("No results found for this query.")
                return

            # Render results in a grid with thumbnails and product details
            for result in results:
                if 'error' in result:
                    st.write(result['error'])
                else:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        # Check if image_url is available; if not, display a placeholder or skip image
                        image_url = result.get("image_url", "")
                        if image_url:
                            st.image(image_url, width=100)
                        else:
                            st.image("https://via.placeholder.com/100", width=100)  # Placeholder image

                    with col2:
                        st.markdown(f"**[{result.get('title', 'Unknown Product')}]({result.get('link', '#')})**")
                        st.write(result.get("description", "No description available"))
                        st.write(f"**Score:** {result.get('score', 0)}")
                    st.markdown("<hr>", unsafe_allow_html=True)






def render_my_handlers():
    st.title("My Handlers")
    st.write("List of your agents and their responses:")
    if "agent_responses" in st.session_state:
        for agent_name, responses in st.session_state.agent_responses.items():
            st.subheader(agent_name)
            for response in responses:
                st.markdown(
                    f"<div style='padding:10px; background-color:#F7F7F7; border:1px solid #DDD; border-radius:5px; margin-bottom:5px;'>"
                    f"{response}</div>", 
                    unsafe_allow_html=True
                )




# Sidebar interaction
st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "Home"}))
st.sidebar.button("My Handlers", on_click=lambda: st.session_state.update({"page": "My Handlers"}))
st.sidebar.button("ShoppingHandler", on_click=lambda: st.session_state.update({"page": "ShoppingHandler"}))