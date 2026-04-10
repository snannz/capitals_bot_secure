import logging
import random
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== ВЕБ-СЕРВЕР ДЛЯ RENDER ==========
app = Flask(name)

@app.route('/')
@app.route('/health')
def health():
    return "Bot is running", 200

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

threading.Thread(target=run_web, daemon=True).start()
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

TOKEN = os.environ.get('TOKEN')

COUNTRIES_DATA = {
    'Европа': {
        'Франция': 'Париж',
        'Германия': 'Берлин',
        'Италия': 'Рим',
        'Испания': 'Мадрид',
        'Великобритания': 'Лондон',
        'Россия': 'Москва',
        'Украина': 'Киев',
        'Польша': 'Варшава',
        'Нидерланды': 'Амстердам',
        'Бельгия': 'Брюссель',
        'Австрия': 'Вена',
        'Швейцария': 'Берн',
        'Швеция': 'Стокгольм',
        'Норвегия': 'Осло',
        'Финляндия': 'Хельсинки',
        'Греция': 'Афины',
        'Португалия': 'Лиссабон',
        'Чехия': 'Прага',
        'Венгрия': 'Будапешт',
        'Румыния': 'Бухарест'
    },
    'Азия': {
        'Китай': 'Пекин',
        'Индия': 'Нью-Дели',
        'Япония': 'Токио',
        'Южная Корея': 'Сеул',
        'Индонезия': 'Джакарта',
        'Таиланд': 'Бангкок',
        'Вьетнам': 'Ханой',
        'Филиппины': 'Манила',
        'Иран': 'Тегеран',
        'Ирак': 'Багдад',
        'Саудовская Аравия': 'Эр-Рияд',
        'Израиль': 'Иерусалим',
        'Турция': 'Анкара',
        'Малайзия': 'Куала-Лумпур',
        'Сингапур': 'Сингапур',
        'Пакистан': 'Исламабад',
        'Бангладеш': 'Дакка',
        'Непал': 'Катманду',
        'Шри-Ланка': 'Шри-Джаяварденепура-Котте'
    },
    'Северная Америка': {
        'США': 'Вашингтон',
        'Канада': 'Оттава',
        'Мексика': 'Мехико',
        'Куба': 'Гавана',
        'Гаити': 'Порт-о-Пренс',
        'Доминиканская Республика': 'Санто-Доминго',
        'Ямайка': 'Кингстон',
        'Багамы': 'Нассау',
        'Коста-Рика': 'Сан-Хосе',
        'Панама': 'Панама',
        'Гватемала': 'Гватемала',
        'Гондурас': 'Тегусигальпа',
        'Никарагуа': 'Манагуа',
        'Сальвадор': 'Сан-Сальвадор'
    },
    'Южная Америка': {
        'Бразилия': 'Бразилиа',
        'Аргентина': 'Буэнос-Айрес',
        'Перу': 'Лима',
        'Колумбия': 'Богота',
        'Венесуэла': 'Каракас',
        'Чили': 'Сантьяго',
        'Эквадор': 'Кито',
        'Боливия': 'Сукре',
        'Парагвай': 'Асунсьон',
        'Уругвай': 'Монтевидео',
        'Гайана': 'Джорджтаун',
        'Суринам': 'Парамарибо'
    },
    'Африка': {
        'Египет': 'Каир',
        'ЮАР': 'Претория',
        'Нигерия': 'Абуджа',
        'Кения': 'Найроби',
        'Марокко': 'Рабат',
        'Алжир': 'Алжир',
        'Тунис': 'Тунис',
        'Эфиопия': 'Аддис-Абеба',
        'Танзания': 'Додома',
        'Гана': 'Аккра',
        'Ангола': 'Луанда',
        'Судан': 'Хартум',
        'Уганда': 'Кампала',
        'Мозамбик': 'Мапуту',
        'Замбия': 'Лусака',
        'Зимбабве': 'Хараре'
    },
    'Австралия и Океания': {
        'Австралия': 'Канберра',
        'Новая Зеландия': 'Веллингтон',
        'Папуа — Новая Гвинея': 'Порт-Морсби',
        'Фиджи': 'Сува',
        'Соломоновы Острова': 'Хониара',
        'Вануату': 'Порт-Вила',
        'Самоа': 'Апиа',
        'Тонга': 'Нукуалофа',
        'Кирибати': 'Южная Тарава',
        'Микронезия': 'Паликир',
        'Маршалловы Острова': 'Маджуро',
        'Палау': 'Нгерулмуд'
    }
}

user_data = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌍 Европа", callback_data='continent_Европа')],
        [InlineKeyboardButton("🌏 Азия", callback_data='continent_Азия')],
        [InlineKeyboardButton("🌎 Северная Америка", callback_data='continent_Северная Америка')],
        [InlineKeyboardButton("🌎 Южная Америка", callback_data='continent_Южная Америка')],
        [InlineKeyboardButton("🌍 Африка", callback_data='continent_Африка')],
        [InlineKeyboardButton("🌏 Австралия и Океания", callback_data='continent_Австралия и Океания')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '🌟 Добро пожаловать в бот для изучения столиц мира!\n\n'
        'Выберите континент, чтобы начать:',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith('continent_'):
        continent = query.data.replace('continent_', '')
        countries = COUNTRIES_DATA[continent]
        user_data[user_id] = {
            'continent': continent,
            'countries': list(countries.keys()),
            'current_country': None,
            'score': 0,
            'total': 0
        }
        countries_list = "\n".join([f"• {country} — {capital}" for country, capital in countries.items()])
        keyboard = [
            [InlineKeyboardButton("▶️ Начать викторину", callback_data='start_quiz')],
            [InlineKeyboardButton("🔙 Назад к выбору континента", callback_data='back_to_continents')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"📚 Вы выбрали: *{continent}*\n\n"
            f"Список стран и столиц:\n{countries_list}\n\n"
            f"Готовы проверить свои знания?",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    elif query.data == 'start_quiz':
        await ask_question(query, user_id)
    elif query.data == 'back_to_continents':
        await show_continents(query)
    elif query.data.startswith('answer_'):
        await handle_answer(query, user_id)

async def show_continents(query):
    keyboard = [
        [InlineKeyboardButton("🌍 Европа", callback_data='continent_Европа')],
        [InlineKeyboardButton("🌏 Азия", callback_data='continent_Азия')],
        [InlineKeyboardButton("🌎 Северная Америка", callback_data='continent_Северная Америка')],
        [InlineKeyboardButton("🌎 Южная Америка", callback_data='continent_Южная Америка')],
        [InlineKeyboardButton("🌍 Африка", callback_data='continent_Африка')],
        [InlineKeyboardButton("🌏 Австралия и Океания", callback_data='continent_Австралия и Океания')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Выберите континент:', reply_markup=reply_markup)

async def ask_question(query, user_id):
    user = user_data.get(user_id)
    if not user:
        await query.edit_message_text("Произошла ошибка. Начните заново с /start")
        return
    available_countries = user['countries']
    if not available_countries:
        await show_results(query, user_id)
        return
    country = random.choice(available_countries)
    correct_capital = COUNTRIES_DATA[user['continent']][country]
    all_capitals = list(COUNTRIES_DATA[user['continent']].values())
    wrong_options = random.sample([c for c in all_capitals if c != correct_capital], min(3, len(all_capitals)-1))
    while len(wrong_options) < 3:
        for other_continent in COUNTRIES_DATA:
            if other_continent != user['continent']:
                other_capitals = list(COUNTRIES_DATA[other_continent].values())
wrong_options.extend(random.sample(other_capitals, min(3 - len(wrong_options), len(other_capitals))))
    options = [correct_capital] + wrong_options[:3]
    random.shuffle(options)
    user['current_country'] = country
    user['current_correct'] = correct_capital
    keyboard = []
    for option in options:
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{option}')])
    keyboard.append([InlineKeyboardButton("❌ Завершить", callback_data='end_quiz')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    progress = f"Прогресс: {user['score']}/{len(user['countries'])} правильных ответов"
    await query.edit_message_text(
        f"❓ Какая столица у страны *{country}*?\n\n{progress}",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_answer(query, user_id):
    user = user_data.get(user_id)
    if not user:
        await query.edit_message_text("Произошла ошибка. Начните заново с /start")
        return
    selected_answer = query.data.replace('answer_', '')
    correct = selected_answer == user['current_correct']
    if user['current_country'] in user['countries']:
        user['countries'].remove(user['current_country'])
    user['total'] += 1
    if correct:
        user['score'] += 1
        message = f"✅ Правильно! {user['current_country']} — {user['current_correct']}\n\n"
    else:
        message = f"❌ Неправильно! {user['current_country']} — {user['current_correct']}\n\n"
    if user['countries']:
        keyboard = [[InlineKeyboardButton("➡️ Следующий вопрос", callback_data='next_question')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message += f"Текущий счет: {user['score']}/{user['total']}"
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        await show_results(query, user_id, message)

async def next_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    await ask_question(query, user_id)

async def show_results(query, user_id, prev_message=""):
    user = user_data.get(user_id)
    if not user:
        await query.edit_message_text("Произошла ошибка. Начните заново с /start")
        return
    percentage = (user['score'] / user['total'] * 100) if user['total'] > 0 else 0
    keyboard = [
        [InlineKeyboardButton("🔄 Пройти заново (тот же континент)", callback_data=f'continent_{user["continent"]}')],
        [InlineKeyboardButton("🌍 Выбрать другой континент", callback_data='back_to_continents')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"{prev_message}\n"
        f"🎉 Викторина завершена!\n\n"
        f"📊 Ваш результат: {user['score']} из {user['total']}\n"
        f"📈 Процент правильных ответов: {percentage:.1f}%\n\n"
        f"Хотите попробовать еще раз?",
        reply_markup=reply_markup
    )

async def end_quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    await show_results(query, user_id)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='^(continent_|start_quiz|back_to_continents|answer_)'))
    application.add_handler(CallbackQueryHandler(next_question_handler, pattern='^next_question$'))
    application.add_handler(CallbackQueryHandler(end_quiz_handler, pattern='^end_quiz$'))
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == 'main':
    main()
