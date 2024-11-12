import os
import serpapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ShoppingHandler:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")  # Load SerpApi key from environment variables
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Initialize an embedding model

    def get_search_results(self, query):
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google"  # Specify the engine type for SerpApi
        }

        try:
            search = serpapi.search(params)
            results = search.as_dict()
            return results.get("organic_results", [])[:10]  # Get the top 10 results
        except Exception as e:
            return [{"title": "Error", "link": str(e)}]

    def get_embedding(self, text):
        # Use the SentenceTransformer model to generate embeddings
        return self.model.encode(text)

    def search(self, query):
        # Fetch the top 10 search results
        results = self.get_search_results(query)
        query_embedding = self.get_embedding(query)

        # Calculate similarity scores for each result
        results_with_scores = []
        for result in results:
            title = result.get("title", "")
            description = result.get("snippet", "")
            content = f"{title}. {description}"
            result_embedding = self.get_embedding(content)
            similarity_score = cosine_similarity([query_embedding], [result_embedding])[0][0]

            results_with_scores.append({
                "title": title,
                "link": result.get("link", ""),
                "score": similarity_score
            })

        # Sort results by similarity score in descending order
        sorted_results = sorted(results_with_scores, key=lambda x: x["score"], reverse=True)
        
        # Return sorted results
        return sorted_results
