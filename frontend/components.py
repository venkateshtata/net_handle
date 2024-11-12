import streamlit as st
from backend.agent_manager import AgentManager

agent_manager = AgentManager()

def render_search_bar():
    # Create a search bar input field
    search_query = st.text_input("Search Agents", placeholder="Type here to search...")

    if search_query:
        matching_agents = [name for name in agent_manager.agents.keys() if search_query.lower() in name.lower()]
        
        if matching_agents:
            for agent_name in matching_agents:
                if st.button(f"Use {agent_name}"):
                    st.session_state.page = agent_name  # Navigate to the agent's page when selected
        else:
            st.write("No matching agents found.")

def render_sidebar():
    # Sidebar title
    st.sidebar.markdown("<h2 style='color: #E5E5E5;'>Menu</h2>", unsafe_allow_html=True)

    # Enhanced CSS for sidebar buttons with icons
    st.sidebar.markdown(
        """
        <style>
        .sidebar-button {
            border: none;
            padding: 10px 20px;
            width: 100%;
            background-color: #333333;
            color: #FFFFFF;
            font-size: 16px;
            text-align: left;
            display: flex;
            align-items: center;
            cursor: pointer;
            margin-bottom: 5px;
        }
        .sidebar-button:hover {
            background-color: #444444;
        }
        .sidebar-icon {
            margin-right: 8px;
        }
        </style>
        <button class="sidebar-button"><span class="sidebar-icon">🏠</span> Home</button>
        <button class="sidebar-button"><span class="sidebar-icon">🛠️</span> My Handlers</button>
        <button class="sidebar-button"><span class="sidebar-icon">⚙️</span> Profile Settings</button>
        """,
        unsafe_allow_html=True
    )
