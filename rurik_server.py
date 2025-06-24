import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def is_important(subject, body):
    keywords = ["urgent", "asap", "important", "deadline", "friday"]
    combined = (subject + " " + body).lower()
    return any(keyword in combined for keyword in keywords)

@app.route('/email', methods=['POST'])
def receive_email():
    print("✅ /email endpoint hit")  # Debug: confirm the route is reached

    data = request.get_json()
    subject = data.get('subject', '')
    body    = data.get('body', '')

    important = is_important(subject, body)
    if important:
        print("📬 Important email received!")
    else:
        print("📪 Not important.")

    # Summarize the email via Ollama if it’s important
    summary = None
    if important:
        ollama_payload = {
            "model": "llama3.2:latest",    # your exact model name
            "prompt": f"Summarize this email:\nSubject: {subject}\n\n{body}",
            "stream": False
        }
        try:
            resp = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json=ollama_payload
            )
            if resp.ok:
                # Ollama returns its text in "response"
                summary = resp.json().get("response", "").strip()
                print(f"✂️ Summary: {summary}")
            else:
                print(f"⚠️ Ollama error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"⚠️ Error calling Ollama: {e}")

    return jsonify({
        "received": True,
        "important": important,
        "summary": summary
    })

if __name__ == '__main__':
    # Bind to IPv4 loopback and disable the auto-reloader
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False
    )
