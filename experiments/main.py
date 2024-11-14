# main.py

from experiments.agents.shopping_agent import ShoppingAgent

def run_shopping_query():
    print("Inside run_shopping_query")
    query = input("Enter your shopping query: ")
    image_path = input("Enter the path to the reference product image (or press Enter to skip): ")
    image_path = image_path if image_path else None

    agent = ShoppingAgent()
    results = agent.handle_query(query, image_path)

    if isinstance(results, list):  # When results are multiple items like stores
        print("\nResults:")
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            if 'image' in result:
                print(f"Image: {result['image']}")
            print()
    else:
        print(f"Response: {results}")  # For single text-based responses

if __name__ == "__main__":
    run_shopping_query()
