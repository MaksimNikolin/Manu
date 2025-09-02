import requests

def sayqalchi(endpoint: str,
              text: str,
              source_lang: str,
              target_lang: str,
              token: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    data = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "model": "sayqalchi"
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['translated_text']
    else:
        return response.json()
