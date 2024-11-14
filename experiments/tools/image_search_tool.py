# tools/image_search_tool.py

class ImageSearchTool:
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def search_similar_items(self, image_path, color=None):
        """Search for similar items based on image content and optional color."""
        prompt = "Show similar items"
        if color:
            prompt += f" in {color} color"

        # Use Groq's process_image to get similar items based on the image and color
        return self.groq_client.process_image(image_path, prompt)
