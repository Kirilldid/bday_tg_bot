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
        "options": ["Joe's Pizza", "Mario's Diner", "The Corner Pub", "Pasta Palace"],
        "answer": 0,
        "image": "https://cdn.pixabay.com/photo/2017/08/06/08/55/key-chain-2590442_1280.jpg",
        "correct_feedback": "✅ You remembered! Joe's Pizza was our spot!",
        "incorrect_feedback": "❌ Oh no! It was Joe's Pizza, not this one!"
    },
    {
        "question": "Who always forgets their wallet when we go out?",
        "hint": "(Hint: Classic move since 2018!)",
        "options": ["Alex", "Chris", "Jordan", "Emma"],
        "answer": 1,
        "image": "https://cdn.pixabay.com/photo/2019/11/14/03/22/shocked-4625235_1280.png",
        "correct_feedback": "✅ Yep, Chris always forgets his wallet!",
        "incorrect_feedback": "❌ Nope! It was Chris who always forgets!"
    },
    {
        "question": "Which inside joke do we use for bad movie nights?",
        "hint": "(Hint: Named after that terrible horror film we watched)",
        "options": ["Project X", "The Rick Special", "Spooky Time", "Late Night Horror"],
        "answer": 1,
        "image": "https://cdn.pixabay.com/photo/2020/03/18/06/34/smiley-4942893_1280.png",
        "correct_feedback": "✅ You got it! The Rick Special is what we call it!",
        "incorrect_feedback": "❌ Nope, it was 'The Rick Special!'"
    },
    {
        "question": "What’s the name of our favorite hiking trail?",
        "hint": "(Hint: We hiked it last summer)",
        "options": ["Eagle’s Peak", "Mountainview Trail", "Forest Loop", "River Path"],
        "answer": 2,
        "image": "https://cdn.pixabay.com/photo/2016/12/16/00/35/winter-1916092_1280.jpg",
        "correct_feedback": "✅ Correct! Forest Loop was our summer adventure!",
        "incorrect_feedback": "❌ It’s actually Forest Loop, we hiked it last summer!"
    },
    {
        "question": "What was the name of the song we always sing at karaoke?",
        "hint": "(Hint: It's a classic rock anthem)",
        "options": ["Bohemian Rhapsody", "Livin’ on a Prayer", "Sweet Caroline", "I Will Survive"],
        "answer": 0,
        "image": "https://cdn.pixabay.com/photo/2015/05/10/16/14/karaoke-759476_1280.jpg",
        "correct_feedback": "✅ Bohemian Rhapsody – the song we rocked at karaoke!",
        "incorrect_feedback": "❌ Oh, it’s Bohemian Rhapsody we always sing!"
    },
    {
        "question": "What’s our secret code for the best party?",
        "hint": "(Hint: It involves a famous drink)",
        "options": ["Rum Punch", "Margarita Madness", "Tequila Sunrise", "Pina Colada Party"],
        "answer": 3,
        "image": "https://cdn.pixabay.com/photo/2017/08/30/02/00/drinks-2692222_1280.jpg",
        "correct_feedback": "✅ You nailed it! Pina Colada Party is our code!",
        "incorrect_feedback": "❌ Nope, it's Pina Colada Party, we’ve said it a hundred times!"
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
        bot.send_message(chat_id, q_data["correct_feedback"])
    else:
        bot.answer_callback_query(call.id, "❌ Wrong answer!")
        bot.send_message(chat_id, q_data["incorrect_feedback"])

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
