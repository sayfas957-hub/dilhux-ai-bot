
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")


# 🧠 Memory
memory = {}


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🤖 AI بىلەن پاراڭلىشىش"],
        ["🌐 تەرجىمە", "📝 يېزىق ياردىمى"],
        ["ℹ️ ياردەم"]
    ]

    menu = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "ئەسسالامۇ ئەلەيكۇم 👋\n\n"
        "مەن ئۇيغۇرچە AI ياردەمچى 🤖\n"
        "سىز بىلەن سۆھبەتلىشىپ، ياردەم بېرەلەيمەن.",
        reply_markup=menu
    )


# AI
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.message.chat.id


    # 🧠 Memory ساقلاش
    if user_id not in memory:
        memory[user_id] = []


    if text == "ℹ️ ياردەم":
        await update.message.reply_text(
            "🤖 AI - سوئال سوراڭ\n"
            "🌐 تەرجىمە - تىل تەرجىمە قىلىش\n"
            "📝 يېزىق ياردىمى - خەت ۋە ماقالە يېزىش"
        )
        return


    if text == "🌐 تەرجىمە":
        await update.message.reply_text(
            "🌐 تەرجىمە ھالىتى\n\n"
            "تەرجىمە قىلماقچى بولغان تېكىستنى يېزىڭ."
        )
        return


    if text == "📝 يېزىق ياردىمى":
        await update.message.reply_text(
            "📝 يېزىق ياردىمى\n\n"
            "ماڭا نېمە يېزىش كېرەكلىكىنى ئېيتىڭ، ياردەم قىلىمەن."
        )
        return


    memory[user_id].append({
        "role": "user",
        "content": text
    })


    # ئەڭ ئاخىرقى 10 پاراڭنى ساقلاش
    conversation = memory[user_id][-10:]


    messages = [
        {
            "role": "system",
            "content":
            "سەن ئۇيغۇرچە AI ياردەمچى. "
            "ئىشلەتكۈچى بىلەن دوستانە ۋە چۈشىنىشلىك پاراڭلاش. "
            "ئىمكانقەدەر ئۇيغۇرچە جاۋاب بەر."
        }
    ]

    messages.extend(conversation)


    url = "https://api.groq.com/openai/v1/chat/completions"


    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }


    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages
    }


    response = requests.post(
        url,
        headers=headers,
        json=data
    )


    result = response.json()


    try:
        answer = result["choices"][0]["message"]["content"]

    except:
        answer = "كەچۈرۈڭ، ھازىر مەسىلە كۆرۈلدى."


    # AI جاۋابىنىمۇ Memory غا قوشۇش
    memory[user_id].append({
        "role": "assistant",
        "content": answer
    })


    await update.message.reply_text(answer)



app = Application.builder().token(TELEGRAM_TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)


app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)


print("AI Bot ئىشلەۋاتىدۇ...")


app.run_polling()
