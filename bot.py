import logging
import random
import os
TOKEN = os.environ.get('TOKEN')
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Данные о странах и столицах по континентам
COUNTRIES_DATA = {
    'Европа': {
        'Австрия': 'Вена',
        'Албания': 'Тирана',
        'Андорра': 'Андорра-ла-Велья',
        'Беларусь': 'Минск',
        'Бельгия': 'Брюссель',
        'Болгария': 'София',
        'Босния и Герцеговина': 'Сараево',
        'Ватикан': 'Ватикан',
        'Великобритания': 'Лондон',
        'Венгрия': 'Будапешт',
        'Германия': 'Берлин',
        'Греция': 'Афины',
        'Дания': 'Копенгаген',
        'Ирландия': 'Дублин',
        'Исландия': 'Рейкьявик',
        'Испания': 'Мадрид',
        'Италия': 'Рим',
        'Латвия': 'Рига',
        'Литва': 'Вильнюс',
        'Лихтенштейн': 'Вадуц',
        'Люксембург': 'Люксембург',
        'Мальта': 'Валлетта',
        'Молдова': 'Кишинёв',
        'Монако': 'Монако',
        'Нидерланды': 'Амстердам',
        'Норвегия': 'Осло',
        'Польша': 'Варшава',
        'Португалия': 'Лиссабон',
        'Россия': 'Москва',
        'Румыния': 'Бухарест',
        'Сан-Марино': 'Сан-Марино',
        'Северная Македония': 'Скопье',
        'Сербия': 'Белград',
        'Словакия': 'Братислава',
        'Словения': 'Любляна',
        'Украина': 'Киев',
        'Финляндия': 'Хельсинки',
        'Франция': 'Париж',
        'Хорватия': 'Загреб',
        'Черногория': 'Подгорица',
        'Чехия': 'Прага',
        'Швейцария': 'Берн',
        'Швеция': 'Стокгольм',
        'Эстония': 'Таллин',
        # дополнительно (частично признанные, но часто включаемые)
        'Косово': 'Приштина',
    },
    # ---------- АЗИЯ (49 стран) ----------
    'Азия': {
        'Азербайджан': 'Баку',
        'Армения': 'Ереван',
        'Афганистан': 'Кабул',
        'Бангладеш': 'Дакка',
        'Бахрейн': 'Манама',
        'Бруней': 'Бандар-Сери-Бегаван',
        'Бутан': 'Тхимпху',
        'Восточный Тимор': 'Дили',
        'Вьетнам': 'Ханой',
        'Грузия': 'Тбилиси',
        'Израиль': 'Иерусалим',
        'Индия': 'Нью-Дели',
        'Индонезия': 'Джакарта',
        'Иордания': 'Амман',
        'Ирак': 'Багдад',
        'Иран': 'Тегеран',
        'Йемен': 'Сана',
        'Казахстан': 'Астана',
        'Камбоджа': 'Пномпень',
        'Катар': 'Доха',
        'Кипр': 'Никосия',
        'Киргизия': 'Бишкек',
        'Китай': 'Пекин',
        'КНДР (Северная Корея)': 'Пхеньян',
        'Кувейт': 'Эль-Кувейт',
        'Лаос': 'Вьентьян',
        'Ливан': 'Бейрут',
        'Малайзия': 'Куала-Лумпур',
        'Мальдивы': 'Мале',
        'Монголия': 'Улан-Батор',
        'Мьянма': 'Нейпьидо',
        'Непал': 'Катманду',
        'ОАЭ': 'Абу-Даби',
        'Оман': 'Маскат',
        'Пакистан': 'Исламабад',
        'Саудовская Аравия': 'Эр-Рияд',
        'Сингапур': 'Сингапур',
        'Сирия': 'Дамаск',
        'Таджикистан': 'Душанбе',
        'Таиланд': 'Бангкок',
        'Туркменистан': 'Ашхабад',
        'Турция': 'Анкара',
        'Узбекистан': 'Ташкент',
        'Филиппины': 'Манила',
        'Шри-Ланка': 'Шри-Джаяварденепура-Котте',
        'Южная Корея': 'Сеул',
        'Япония': 'Токио',
        # дополнительные
        'Палестина': 'Рамалла (адм.)',
        'Тайвань': 'Тайбэй',
    },
    # ---------- АФРИКА (54 страны) ----------
    'Африка': {
        'Алжир': 'Алжир',
        'Ангола': 'Луанда',
        'Бенин': 'Порто-Ново',
        'Ботсвана': 'Габороне',
        'Буркина-Фасо': 'Уагадугу',
        'Бурунди': 'Гитега',
        'Габон': 'Либревиль',
        'Гамбия': 'Банжул',
        'Гана': 'Аккра',
        'Гвинея': 'Конакри',
        'Гвинея-Бисау': 'Бисау',
        'Джибути': 'Джибути',
        'Египет': 'Каир',
        'Замбия': 'Лусака',
        'Зимбабве': 'Хараре',
        'Кабо-Верде': 'Прая',
        'Камерун': 'Яунде',
        'Кения': 'Найроби',
        'Коморы': 'Морони',
        'ДР Конго': 'Киншаса',
        'Республика Конго': 'Браззавиль',
        'Кот-д’Ивуар': 'Ямусукро',
        'Лесото': 'Масеру',
        'Либерия': 'Монровия',
        'Ливия': 'Триполи',
        'Маврикий': 'Порт-Луи',
        'Мавритания': 'Нуакшот',
        'Мадагаскар': 'Антананариву',
        'Малави': 'Лилонгве',
        'Мали': 'Бамако',
        'Марокко': 'Рабат',
        'Мозамбик': 'Мапуту',
        'Намибия': 'Виндхук',
        'Нигер': 'Ниамей',
        'Нигерия': 'Абуджа',
        'Руанда': 'Кигали',
        'Сан-Томе и Принсипи': 'Сан-Томе',
        'Сейшельские Острова': 'Виктория',
        'Сенегал': 'Дакар',
        'Сомали': 'Могадишо',
        'Судан': 'Хартум',
        'Сьерра-Леоне': 'Фритаун',
        'Танзания': 'Додома',
        'Того': 'Ломе',
        'Тунис': 'Тунис',
        'Уганда': 'Кампала',
        'ЦАР': 'Банги',
        'Чад': 'Нджамена',
        'Экваториальная Гвинея': 'Малабо',
        'Эритрея': 'Асмэра',
        'Эсватини': 'Мбабане',
        'Эфиопия': 'Аддис-Абеба',
        'ЮАР': 'Претория',
        'Южный Судан': 'Джуба',
    },
 # ---------- СЕВЕРНАЯ АМЕРИКА (23 страны) ----------
    'Северная Америка': {
        'Антигуа и Барбуда': 'Сент-Джонс',
        'Багамы': 'Нассау',
        'Барбадос': 'Бриджтаун',
        'Белиз': 'Бельмопан',
        'Гаити': 'Порт-о-Пренс',
        'Гватемала': 'Гватемала',
        'Гондурас': 'Тегусигальпа',
        'Гренада': 'Сент-Джорджес',
        'Доминика': 'Розо',
        'Доминиканская Республика': 'Санто-Доминго',
        'Канада': 'Оттава',
        'Коста-Рика': 'Сан-Хосе',
        'Куба': 'Гавана',
        'Мексика': 'Мехико',
        'Никарагуа': 'Манагуа',
        'Панама': 'Панама',
        'Сальвадор': 'Сан-Сальвадор',
        'Сент-Винсент и Гренадины': 'Кингстаун',
        'Сент-Китс и Невис': 'Бастер',
        'Сент-Люсия': 'Кастри',
        'США': 'Вашингтон',
        'Тринидад и Тобаго': 'Порт-оф-Спейн',
        'Ямайка': 'Кингстон',
    },
    # ---------- ЮЖНАЯ АМЕРИКА (12 стран) ----------
    'Южная Америка': {
        'Аргентина': 'Буэнос-Айрес',
        'Боливия': 'Сукре',
        'Бразилия': 'Бразилиа',
        'Венесуэла': 'Каракас',
        'Гайана': 'Джорджтаун',
        'Колумбия': 'Богота',
        'Парагвай': 'Асунсьон',
        'Перу': 'Лима',
        'Суринам': 'Парамарибо',
        'Уругвай': 'Монтевидео',
        'Чили': 'Сантьяго',
        'Эквадор': 'Кито',
    },
    # ---------- АВСТРАЛИЯ И ОКЕАНИЯ (14 стран) ----------
    'Австралия и Океания': {
        'Австралия': 'Канберра',
        'Вануату': 'Порт-Вила',
        'Кирибати': 'Южная Тарава',
        'Маршалловы Острова': 'Маджуро',
        'Микронезия': 'Паликир',
        'Науру': 'Ярен',
        'Новая Зеландия': 'Веллингтон',
        'Палау': 'Нгерулмуд',
        'Папуа — Новая Гвинея': 'Порт-Морсби',
        'Самоа': 'Апиа',
        'Соломоновы Острова': 'Хониара',
        'Тонга': 'Нукуалофа',
        'Тувалу': 'Фунафути',
        'Фиджи': 'Сува',
    }
}

# Хранилище данных пользователей
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветственное сообщение и показывает выбор континентов."""
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
    """Обрабатывает нажатия на кнопки."""
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
    user['options'] = options
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

if __name__ == '__main__':
    main()