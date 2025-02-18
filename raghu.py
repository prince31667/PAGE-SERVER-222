from flask import Flask, request, render_template_string
import os
import threading
import time
import requests

app = Flask(__name__)

# Data directory
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TOKEN_FILE = os.path.join(DATA_DIR, "tokens.txt")
MESSAGE_FILE = os.path.join(DATA_DIR, "messages.txt")
TIME_FILE = os.path.join(DATA_DIR, "time.txt")
GROUP_ID_FILE = os.path.join(DATA_DIR, "group_id.txt")

# Function to save uploaded files
def save_file(file, path):
    with open(path, "wb") as f:
        f.write(file.read())

# Function to send messages using multiple tokens
def send_messages(hater_name, group_id):
    try:
        with open(TOKEN_FILE, "r") as f:
            tokens = [line.strip() for line in f.readlines() if line.strip()]

        with open(MESSAGE_FILE, "r") as f:
            messages = [line.strip() for line in f.readlines() if line.strip()]

        with open(TIME_FILE, "r") as f:
            delay = int(f.read().strip())

        if not (tokens and messages):
            print("[!] Tokens or Messages file is empty.")
            return

        if not group_id:
            print("[!] Group Chat ID is missing!")
            return

        while True:
            for token, message in zip(tokens, messages):
                full_message = f"{hater_name}: {message}"  # Hater Name पहले जोड़ा जाएगा
                url = f"https://graph.facebook.com/v15.0/t_{group_id}/"
                headers = {'User-Agent': 'Mozilla/5.0'}
                payload = {'access_token': token, 'message': full_message}

                response = requests.post(url, json=payload, headers=headers)
                if response.ok:
                    print(f"[+] Message sent: {full_message}")
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
    <title>Carter by Rocky Roy</title>
    <style>
        body { background-color: black; color: white; font-family: Arial, sans-serif; text-align: center; }
        .container { background: #222; max-width: 400px; margin: 50px auto; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(255, 255, 255, 0.2); }
        h1 { color: #ffcc00; }
        form { display: flex; flex-direction: column; }
        label { text-align: left; font-weight: bold; margin: 10px 0 5px; }
        input, button { padding: 10px; border-radius: 5px; margin-bottom: 10px; }
        button { background-color: #ffcc00; color: black; border: none; cursor: pointer; }
        button:hover { background-color: #ff9900; }
        footer { margin-top: 20px; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Carter by Rocky Roy</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <label>Upload Tokens File:</label>
            <input type="file" name="token_file" required>

            <label>Upload Messages File:</label>
            <input type="file" name="message_file" required>

            <label>Enter Hater Name:</label>
            <input type="text" name="hater_name" required>

            <label>Enter Group Chat ID:</label>
            <input type="text" name="group_id" required>

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
        token_file = request.files.get("token_file")
        message_file = request.files.get("message_file")
        hater_name = request.form.get("hater_name")
        group_id = request.form.get("group_id")
        delay = request.form.get("delay", 5)

        if token_file and message_file and hater_name and group_id:
            save_file(token_file, TOKEN_FILE)
            save_file(message_file, MESSAGE_FILE)
            with open(TIME_FILE, "w") as f:
                f.write(str(delay))
            with open(GROUP_ID_FILE, "w") as f:
                f.write(group_id)

            threading.Thread(target=send_messages, args=(hater_name, group_id), daemon=True).start()

    return render_template_string(HTML_TEMPLATE)

# Start Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
