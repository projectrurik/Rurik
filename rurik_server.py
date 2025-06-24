from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def summarize_email(prompt):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": f"Summarize this email and say if it's important:\n\n{prompt}",
            "stream": False
        })
        return response.json().get("response", "No response from LLM.")
    except Exception as e:
        return f"Error calling LLM: {str(e)}"

@app.route('/email', methods=['POST'])
def handle_email():
    print("✅ /email endpoint was hit!")
    data = request.get_json()
    if not data or 'subject' not in data or 'body' not in data:
        return jsonify({"error": "Missing 'subject' or 'body' in request"}), 400

    print(f"📧 New email received: {data['subject']}")
    result = summarize_email(f"Subject: {data['subject']}\n\n{data['body']}")
    
    return jsonify({"summary": result})

if __name__ == '__main__':
    print("🌐 Rurik server is running at http://localhost:5000")
    app.run(debug=True)
