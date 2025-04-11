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
        "question": "Продолжите фразу: «Неблагозвучно и...»",
        "options": ["Социально ненормально", "Асоциально терпимо", "Социально неприемлемо", "Хуй с ним!"],
        "answer": 2,
        "image": "https://i.ibb.co/B5gNxF2j/IMG-3116.png",
        "correct_feedback": "✅ Правильно! Знаешь классику!",
        "incorrect_feedback": "❌ Неправильно! Видимо, ты во время этого спора спал."
    },
    {
        "question": "Как зовут этого персонажа?",
        "options": ["Миша", "Саша", "Дима", "Дэн Рейнольдс"],
        "answer": 1,
        "image": "https://i.ibb.co/Xkb7TNFW/IMG-3104.png",
        "correct_feedback": "✅ Правильно! Помнишь всех!",
        "incorrect_feedback": "❌ Неправильно! Забыл легенду..."
    },
    {
        "question": "Кто скрыт на фото?",
        "options": ["Илья", "Дэнил", "Кирилл", "Дядя Игорь"],
        "answer": 0,
        "image": "https://i.ibb.co/cX7kXrCY/IMG-2858.png",
        "correct_feedback": "✅ Правильно! Может, это ты фоткал?",
        "incorrect_feedback": "❌ Неправильно! Видимо, тебя там не было."
    },
    {
        "question": "С какой тусовки это легендарное фото?",
        "options": ["ДР В ПУСТОТЕ", "ДР В ДУХНОТЕ", "ДР У КАМИНА", "Это вообще Никольск"],
        "answer": 0,
        "image": "https://i.ibb.co/fVR4s5GY/IMG-0604.jpg",
        "correct_feedback": "✅ Правильно! Это было легко!",
        "incorrect_feedback": "❌ Неправильно! Как можно забыть такую классику?"
    },
    {
        "question": "С какой тусовки это фото?",
        "options": ["ДР В ПУСТОТЕ", "ДР НА ВОДЕ", "ДР У КАМИНА", "Праздник фонариков 2005"],
        "answer": 2,
        "image": "https://i.ibb.co/fGKS9RYP/IMG-6949.jpg",
        "correct_feedback": "✅ Правильно! Неужели ты и это помнишь?",
        "incorrect_feedback": "❌ Неправильно! Сразу видно, кто не колол дрова в тот раз."
    },
    {
        "question": "Под какую песню мы носились в 5 утра по полю?",
        "options": ["Life is life", "You can't always get what you want", "Satisfaction", "Вот и помер дед Максим"],
        "answer": 1,
        "image": "https://i.ibb.co/bwGGC54/IMG-2954.jpg",
        "correct_feedback": "✅ Правильно! Не забыл, даже несмотря на то, что мы бухали всю ночь!",
        "incorrect_feedback": "❌ Неправильно! Ну и неудивительно — мы же бухали всю ночь..."
    },
    {
        "question": "Кто под маской кабана?",
        "options": ["Коля", "Вася", "Дэнил", "Никто, это настоящий кабан"],
        "answer": 0,
        "image": "https://i.ibb.co/bg2b8wBG/IMG-6995.png",
        "correct_feedback": "✅ Правильно! Кто же еще это может быть?",
        "incorrect_feedback": "❌ Неправильно! Неужели даже красные штаны не подсказали?"
    },
    {
        "question": "Как называлась команда Лехи и Дэнила, когда мы играли в ассоциации в бане?",
        "options": ["Тюлени-космонавты", "Моржи-любовники", "Пингвины-испытатели", "Айтишники-пидоры"],
        "answer": 1,
        "image": "https://i.ibb.co/wFbdS5rq/2025-04-05-18-46-47.jpg",
        "correct_feedback": "✅ Правильно! Как ты вообще это помнишь?",
        "incorrect_feedback": "❌ Неправильно! Но и неудивительно, вряд ли кто-то, кроме автора вопроса, это помнит."
    },
    {
        "question": "На какой нашей тусовке впервые появился Асхат?",
        "options": ["ДР В ПУСТОТЕ", "ДР НА КРЫШЕ", "ДР В ДУХОТЕ - ДВЕ БАШНИ", "Кто такой Асхат?"],
        "answer": 1,
        "image": "https://i.ibb.co/JjtQvn5K/IMG-1378.jpg",
        "correct_feedback": "✅ Правильно! Ты что ли был там?",
        "incorrect_feedback": "❌ Неправильно! Немногие вспомнят..."
    },
    {
        "question": "Сколько пальцев рома нужно на один стакан Кокосового Стэнли?",
        "options": ["Два", "Три", "Четыре", "Шестнадцать"],
        "answer": 1,
        "image": "https://i.ibb.co/DSGshh5/IMG-6955.jpg",
        "correct_feedback": "✅ Правильно! Откуда ты знаешь секретный рецепт?!",
        "incorrect_feedback": "❌ Неправильно! Ну и неудивительно — рецепт-то секретный!"
    },
    {
        "question": "Что на экране?",
        "options": ["Видосы с выпускного", "Мортал комбат", "Футбол", "Серия \"Друзей\" про ДР"],
        "answer": 2,
        "image": "https://i.ibb.co/TMdHMZ9W/image.jpg",
        "correct_feedback": "✅ Правильно! ЧЕ 2024.",
        "incorrect_feedback": "❌ Неправильно! Наверное ты спал."
    },
    {
        "question": "Каким из способов мы НЕ поздравили Дэниэла с др в 2021 году?",
        "options": ["Личными сообщениями", "Во всех беседах всех др", "Голубиной почтой", "Сообщением в сбербанке"],
        "answer": 2,
        "image": "https://ideogram.ai/assets/image/lossless/response/mng6lWOaSl2H05lHK_gtBg",  # временная картинка
        "correct_feedback": "✅ Правильно! Остальные методы были использованы!",
        "incorrect_feedback": "❌ А вот и нет. Ты что, не поздравлял?"
    },
    {
        "question": "Что мы делали накануне?",
        "options": ["Парились в бане", "Жарили шашлыки", "Прятались от ракет", "Играли в нарды"],
        "answer": 2,
        "image": "https://i.ibb.co/NdzJfq6b/photo-2025-04-11-01-08-07.jpg",  # временная картинка
        "correct_feedback": "✅ Правильно! В такой компании было совсем не страшно",
        "incorrect_feedback": "❌ Хочется повторить всё, кроме правильного ответа"
    },
]


user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {"score": 0, "current_q": 0}
    bot.send_message(message.chat.id, "👋 Ответь на несколько вопросов про наши легендарные тусовки. \n\n Так ты докажешь, что ты реально Коля, а не какой-то бот 😏")
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

    bot.send_message(chat_id, f"{q_data['question']}", reply_markup=markup)

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
        result = "🎉 Невероятно! Ты легенда, откуда ты все это знаешь? Может ты составлял этот квиз?"
    elif score >= len(questions) // 2:
        result = "😊 Харош! Много помнишь, хранишь много тепла в своей памяти"
    else:
        result = "😅 Штош... каждется, это повод собраться вновь"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 Попробуем еще раз?", callback_data="restart"))

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
