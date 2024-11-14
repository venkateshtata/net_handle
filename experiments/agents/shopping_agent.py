# agents/shopping_agent.py

from ..groq_integration.llama_groq_client import GroqLlamaClient
from ..tools.serp_search_tool import SerpSearchTool
from ..tools.image_search_tool import ImageSearchTool

class ShoppingAgent:
    def __init__(self):
        self.groq_client = GroqLlamaClient()
        self.serp_tool = SerpSearchTool()
        self.image_tool = ImageSearchTool(self.groq_client)

    def handle_query(self, query, image_path=None):
        print(f'Inside shopping agent.handle_query')
        if "store" in query and image_path:
            print("Processing a store search with image...")
            response = self.groq_client.process_image(image_path, prompt=query)
            stores = self.serp_tool.search_store(response)
            return stores

        elif "similar" in query and image_path:
            print("Processing a similar item search...")
            color = self.extract_color_from_query(query)
            prompt = f"{query}. Looking for similar items in {color} color."
            similar_items = self.groq_client.process_image(image_path, prompt=prompt)
            return similar_items

        else:
            print("Processing a general search...")
            return self.groq_client.process_text(query)

    def extract_color_from_query(self, query):
        colors = ["white", "black", "red", "blue"]
        for color in colors:
            if color in query:
                return color
        return None
