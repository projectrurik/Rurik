# rurik.py

import requests

def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json().get("response", "[No response from model]")

if __name__ == "__main__":
    print("🤖 Rurik is ready. Type something (or 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        reply = query_ollama(user_input)
        print(reply)
