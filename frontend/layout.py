import streamlit as st
from backend.agent_manager import AgentManager
from frontend.components import render_search_bar, render_sidebar

agent_manager = AgentManager()

def render_layout():
    render_sidebar()
    
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        render_home_page()
    elif st.session_state.page == "My Handlers":
        render_my_handlers()
    elif st.session_state.page == "ShoppingHandler":
        render_agent_search_page("ShoppingHandler")

def render_home_page():
    st.title("Welcome to NetHandle")
    render_search_bar()  # Search for available agents

def render_my_handlers():
    st.title("My Handlers")
    st.write("List of your agents and their responses:")
    if "agent_responses" in st.session_state:
        for agent_name, responses in st.session_state.agent_responses.items():
            st.subheader(agent_name)
            for response in responses:
                st.write(response)

def render_agent_search_page(agent_name):
    agent = agent_manager.get_agent(agent_name)
    if agent:
        query = st.text_input(f"Search with {agent_name}", placeholder="Type your query here...")
        if query:
            results = agent.search(query)
            st.session_state.agent_responses.setdefault(agent_name, []).append(results)
            st.write(f"Top results for '{query}' based on similarity:")
            for result in results:
                st.write(f"**{result['title']}** - {result['score']:.2f}")
                st.write(result["link"])


# Sidebar interaction
st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "Home"}))
st.sidebar.button("My Handlers", on_click=lambda: st.session_state.update({"page": "My Handlers"}))
st.sidebar.button("ShoppingHandler", on_click=lambda: st.session_state.update({"page": "ShoppingHandler"}))
