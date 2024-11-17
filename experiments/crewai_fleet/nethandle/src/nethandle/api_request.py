import requests

# Define the API endpoint
url = "http://localhost:8000/process_query"

# Define the query payload
payload = {
    "topic": "How can I manage my morning blood sugar levels?"
}

# Send the POST request
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    # Print the response
    print("Response from model:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
