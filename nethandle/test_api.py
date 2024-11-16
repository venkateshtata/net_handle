import requests

url = "http://127.0.0.1:8000/agent-workflow"
data = {"message": "I need a diabetes-friendly dinner recipe. Can you find one and confirm if it aligns with my health records and medications?"}

response = requests.post(url, json=data)
print(response.json())
