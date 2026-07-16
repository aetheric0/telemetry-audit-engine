import requests

url = "http://127.0.0.1:8000/api/v1/diagnose"
payload: dict[str, str | int] = {
    "query_text": "Is there a node with a current between the range of 15 to 25 Amperes",
    "n_results": 5
}

with requests.post(url, json=payload, stream=True) as response:
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
    else:
        print(response.text)