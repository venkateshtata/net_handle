from agents.shopping_agent import ShoppingHandler

class AgentManager:
    def __init__(self):
        self.agents = {"ShoppingHandler": ShoppingHandler()}

    def get_agent(self, agent_name):
        return self.agents.get(agent_name, None)
