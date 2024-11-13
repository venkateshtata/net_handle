import os
import json
import re
from langchain import OpenAI
from langchain.agents import initialize_agent, load_tools
from langchain_community.utilities import SerpAPIWrapper
from pydantic import BaseModel, ValidationError
from langchain.prompts import PromptTemplate
from typing import List, Optional
import time

class Product(BaseModel):
    position: int
    title: str
    description: Optional[str] = "No description available"
    link: str
    image_url: Optional[str] = ""
    score: float = 0.0

class ShoppingHandler:
    def __init__(self):
        self.llm = OpenAI(temperature=0)

        self.prompt_template_str = """\
You are a product expert. Find a few products related to the query below.

Query: "{query}"

Respond with a JSON array of 3-5 product objects. Each object should have:
- position: Product's position in the list
- title: Product title
- description: A brief description
- link: URL where the product can be found
- image_url: URL of the product image
- score: Relevance score (0-1)

Only include relevant products. Keep responses brief.
"""

        self.prompt_template = PromptTemplate.from_template(self.prompt_template_str)
        tools = load_tools(
            ["serpapi"],
            serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            location="Austin, Texas, United States",
            hl="en",
            gl="us"
        )
        self.agent_executor = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )

    def extract_complete_json_objects(self, response_text: str) -> List[dict]:
        """Extracts and parses individual JSON objects, attempting to fix incomplete JSON arrays."""
        response_text = response_text.replace("'", '"')  # JSON compatibility
        
        try:
            response_data = json.loads(response_text)
            if isinstance(response_data, list):
                # Convert Product objects to dictionaries if needed
                return [product.__dict__ if hasattr(product, "__dict__") else product for product in response_data]
        except json.JSONDecodeError:
            print("Error decoding JSON array, falling back to object extraction.")

        # Fallback to capture JSON objects individually if full array parsing fails
        matches = re.findall(r'\{[^}]*\}', response_text)
        products = []

        for match in matches:
            if not match.endswith('}'):
                match += '}'  # Close any incomplete objects
            try:
                product = json.loads(match)
                products.append(product)
            except json.JSONDecodeError:
                print("Skipping invalid JSON fragment.")

        return products

    def parse_response(self, response: List[dict]) -> List[Product]:
        print("Raw response data received:", response)
        products = []
        try:
            for item in response:
                # Check if item is a dictionary, otherwise convert it
                if isinstance(item, Product):
                    item = item.__dict__
                product = Product(
                    position=item.get("position", 0),
                    title=item.get("title", "Unknown Product"),
                    description=item.get("description", "No description available"),
                    link=item.get("link", ""),
                    image_url=item.get("image_url", ""),
                    score=float(item.get("score", 0))
                )
                products.append(product.__dict__)
            print("Parsed products:", products)
        except ValidationError as e:
            print("Validation error:", e)
        return products

    def search(self, query: str) -> List[Product]:
        max_retries = 3
        retries = 0
        products = []

        while retries < max_retries and not products:
            prompt = self.prompt_template.format(query=query)
            response = self.agent_executor.invoke({"input": prompt, "max_tokens": 150})

            print("Initial response:", response)
            
            response_text = response['output'] if isinstance(response, dict) else str(response)
            print("Raw response text:", response_text)

            response_data = self.extract_complete_json_objects(response_text)
            print("Parsed JSON response data:", response_data)

            products = self.parse_response(response_data) if response_data else []

            if not products:
                print(f"No valid products found. Retrying {retries + 1}/{max_retries}...")
                retries += 1
                time.sleep(2)  # Adding a slight delay before retrying

        # If still no valid products found, return an error message
        if not products:
            products = [{"error": "No valid products found after retries"}]

        return products

# Example usage
shopping_agent = ShoppingHandler()
result = shopping_agent.search("apple watch")
print(result)
