import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat/completions",
    json={
        "stream": True,
        "messages": [{"role": "user", "content": "Hello!"}],
    },
    stream=True,
)
if response.status_code == 200:
    for chunk in response.iter_content(chunk_size=1024):
        print(chunk)
