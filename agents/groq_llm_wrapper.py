# agents/groq_llm_wrapper.py

from langchain.schema.runnable import Runnable
from experiments.groq_integration.llama_groq_client import GroqLlamaClient

class GroqLLMWrapper(Runnable):
    def __init__(self, model_name="llama-3.2-11b-vision-preview"):
        self.client = GroqLlamaClient(model_name=model_name)

    def invoke(self, input_text: str) -> str:
        return self.client.process_text(input_text)

    async def ainvoke(self, input_text: str) -> str:
        # For async compatibility, implement asynchronous call if needed
        return await self.client.process_text(input_text)

    def process_text(self, prompt: str) -> str:
        """Provide compatibility with LangChain's expected method."""
        return self.invoke(prompt)  # Reuse the invoke method for processing the text

