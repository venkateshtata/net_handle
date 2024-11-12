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
            results = search.as_dict()  # Directly get the results dictionary
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
        for index, result in enumerate(results, start=1):
            title = result.get("title", "")
            description = result.get("snippet", "")
            link = result.get("link", "")
            image_url = result.get("thumbnail", "")  # Assuming there's a thumbnail field for image URL
            content = f"{title}. {description}"
            result_embedding = self.get_embedding(content)
            similarity_score = cosine_similarity([query_embedding], [result_embedding])[0][0]

            results_with_scores.append({
                "index": index,
                "title": title,
                "description": description,
                "link": link,
                "image_url": image_url,
                "score": similarity_score
            })

        # Sort results by similarity score in descending order
        sorted_results = sorted(results_with_scores, key=lambda x: x["score"], reverse=True)
        
        # Debug: Print and return the sorted results to verify structure
        print("Debug - Search Results:", sorted_results)
        return sorted_results

