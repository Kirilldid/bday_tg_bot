import os
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Sample questions for the quiz with images
questions = [
    {
        "question": "What did we call our legendary Friday hangout spot?",
        "hint": "(Hint: It had the best cheap pizza!)",
        "options": ["Joe's Pizza", "Mario's Diner", "The Corner Pub"],
        "answer": 0,
        "image": "https://cdn.pixabay.com/photo/2017/08/06/08/55/key-chain-2590442_1280.jpg"  # Placeholder image URL
    },
    {
        "question": "Who always forgets their wallet when we go out?",
        "hint": "(Hint: Classic move since 2018!)",
        "options": ["Alex", "Chris", "Jordan"],
        "answer": 1,
        "image": "https://cdn.pixabay.com/photo/2019/11/14/03/22/shocked-4625235_1280.png"  # Placeholder image URL
    },
    {
        "question": "Which inside joke do we use for bad movie nights?",
        "hint": "(Hint: Named after that terrible horror film we watched)",
        "options": ["Project X", "The Rick Special", "Spooky Time"],
        "answer": 1,
        "image": "https://cdn.pixabay.com/photo/2020/03/18/06/34/smiley-4942893_1280.png"  # Placeholder image URL
    }
]

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"score": 0, "current_q": 0}
    bot.send_message(message.chat.id, "👋 Welcome to the Friendship Quiz!\n\nAnswer 10-15 fun questions about our group's legendary moments.\n\nEach question comes with a hint, and you’ll get feedback after every answer. Let's see how well you remember our adventures!")
    send_question(message.chat.id)

def send_question(chat_id):
    user = user_data.get(chat_id)
    if user["current_q"] >= len(questions):
        return finish_quiz(chat_id)

    q_data = questions[user["current_q"]]
    markup = InlineKeyboardMarkup()

    for idx, option in enumerate(q_data["options"]):
        markup.add(InlineKeyboardButton(option, callback_data=f"answer_{idx}"))

    # Send image if available
    if "image" in q_data and q_data["image"]:
        bot.send_photo(chat_id, q_data["image"])

    bot.send_message(chat_id, f"{q_data['question']}\n{q_data['hint']}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def answer_question(call):
    chat_id = call.message.chat.id
    user = user_data.get(chat_id)

    if not user or user["current_q"] >= len(questions):
        return

    q_data = questions[user["current_q"]]
    selected_option = int(call.data.split("_")[1])
    correct = selected_option == q_data["answer"]

    if correct:
        user["score"] += 1
        bot.answer_callback_query(call.id, "✅ Correct!")
    else:
        bot.answer_callback_query(call.id, "❌ Wrong answer!")

    user["current_q"] += 1
    bot.send_message(chat_id, f"Score: {user['score']} / {user['current_q']}")
    send_question(chat_id)

def finish_quiz(chat_id):
    score = user_data[chat_id]["score"]

    if score == len(questions):
        result = "🎉 Perfect! You're the memory champion!"
    elif score >= len(questions) // 2:
        result = "😊 Not bad! You remember a lot!"
    else:
        result = "😅 Well... maybe it's time for a reunion!"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 Play Again", callback_data="restart"))

    bot.send_message(chat_id, f"Quiz finished! Your final score: {score}/{len(questions)}\n{result}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart_quiz(call):
    chat_id = call.message.chat.id
    user_data[chat_id] = {"score": 0, "current_q": 0}
    send_question(chat_id)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}")
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
