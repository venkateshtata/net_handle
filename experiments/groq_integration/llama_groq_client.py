# groq_integration/llama_groq_client.py
from groq import Groq
import base64
from experiments.config import GROQ_API_KEY

class GroqLlamaClient:
    def __init__(self, model_name="llama-3.2-11b-vision-preview"):
        self.model_name = model_name
        self.client = Groq(api_key='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')

    def process_text(self, prompt):
        print(f'Inside llama_groq_client.process_text with prompt: {prompt}')
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}]}
                ],
                model=self.model_name,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in process_text: {e}")
            return None

    def process_image(self, image_path, prompt):
        print(f'Inside llama_groq_client.process_image with image_path: {image_path}')
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                model=self.model_name,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in process_image: {e}")
            return None
