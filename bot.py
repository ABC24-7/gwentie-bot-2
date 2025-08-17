import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === СОСТОЯНИЯ ИГРЫ ===
user_states = {}  # {user_id: {"chapter": "chapter_1"}}

# === КНОПКИ ===
def get_keyboard(options):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=f"choice_{i}")]
        for i, text in enumerate(options)
    ])

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"chapter": "chapter_1"}

    title = "🌅 Утро в клетке"
    text = ("Ты — Гвинти, обычная, но очень любопытная морская свинка.\n"
            "Хозяин ушёл на работу. Пеппа ещё спит.\n\nЧто ты хочешь сделать?")
    options = [
        "🌿 Съесть сено и начать день с силой!",
        "🔍 Осмотреть клетку — вдруг где-то спрятан секрет?",
        "💤 Повернуться и поспать ещё часок.",
        "🗣️ Разбудить Пеппу и поговорить."
    ]

    await update.message.reply_text(
        f"<b>{title}</b>\n\n{text}",
        reply_markup=get_keyboard(options),
        parse_mode='HTML'
    )

# === ОБРАБОТКА ВЫБОРА ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if user_id not in user_states:
        await query.edit_message_text("Игра сброшена. Начни с /start", reply_markup=None)
        return

    current_chapter = user_states[user_id]["chapter"]
    try:
        choice = int(query.data.split("_")[1])
    except (IndexError, ValueError):
        return

    # === Глава 1 → Глава 2 (сон) ===
    if current_chapter == "chapter_1" and choice == 2:
        user_states[user_id]["chapter"] = "chapter_2_sleep"
        await chapter_2_sleep(query)

    # Можно расширить — пока оставим так
    else:
        await query.edit_message_text(
            "Приключение продолжается... (игра в разработке)",
            reply_markup=get_keyboard(["Продолжить"])
        )

# === Пример следующей сцены ===
async def chapter_2_sleep(query):
    text = ("💤 Ты решаешь поспать…\nНо вдруг — шурш-шурш…\n\n"
            "Пеппа шепчет: *«Гвинти! Я видела, как туда пролезла мышь!»*\n\n"
            "Что будешь делать?")
    options = [
        "🧱 Заделать дыру",
        "🐭 Исследовать!"
    ]
    await query.edit_message_text(
        f"<b>🕳️ Шурш-шурш…</b>\n\n{text}",
        reply_markup=get_keyboard(options),
        parse_mode='HTML'
    )

# === ЗАПУСК БОТА ===
if __name__ == '__main__':
    TOKEN = "YOUR_TOKEN_HERE"  # Render подставит реальный токен
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Бот запущен на Render!")
    app.run_polling()
