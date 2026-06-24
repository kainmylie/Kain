import argparse
import os
import random
import re
import sys

from content import AI_INVITE_TEXT, FACTS, HELP_TEXT, SECTIONS, START_TEXT

try:
    import telebot
    from telebot import types
except ImportError:
    telebot = None
    types = None

try:
    from groq import Groq
except ImportError:
    Groq = None


BUTTON_RANDOM_FACT = "🎲 Рандомный факт обо мне"
BUTTON_AI = "🤖 Спроси Камилу"
BUTTON_MUSIC = "🎧 Атмосфера 𝙺𝚊𝚒𝚗𝚢"
BUTTON_BEAUTY = "Beauty-батл💅🏻"
BUTTON_QUIZ = "🧩 Викторина"
BUTTON_RESTART = "🔄 Рестарт"
BUTTON_RATE = "⭐ Оценить бота"
MUSIC_FILE = "Wild Strawberry.mp3"
HAND_FILE = "Hand.jpeg"

BEAUTY_OPTIONS = ["Kylie Jenner", "Megan Fox", "Irina Shayk", "Adriana Lima"]

RATE_OPTIONS = ["Бот как бот", "Неплохо", "Супер, есть вайб"]

RATE_REACTIONS = {
    "Бот как бот": {
        "gif": "not_funny_cat.gif",
        "text": "…",
    },
    "Неплохо": {
        "gif": "huh_cat.gif",
        "text": "«Неплохо?»",
    },
    "Супер, есть вайб": {
        "gif": "funny_cat.gif",
        "text": "От души!🤪",
    },
}

QUIZ_LETTERS = ["A", "B", "C"]

QUIZ_QUESTIONS = [
    {
        "question": "Почему Камила выбрала Python?",
        "answers": [
            "Потому что высокая скорость работы и строгая структура",
            "Потому что с ним можно создавать разные проекты: ботов, игры и веб-приложения",
            "Потому что он удобен для работы только с сайтами",
        ],
        "right": 1,
    },
    {
        "question": "Было ли Камиле трудно в начале пути?",
        "answers": [
            "Нет, все сразу было легко",
            "Да, очень",
            "Немного, но терпимо",
        ],
        "right": 1,
    },
    {
        "question": "Что лучше всего описывает портфолио-бота Камилы?",
        "answers": [
            "Бот с личной информацией и разделами",
            "Проект с текстами, кнопками и командами",
            "Интерактивный бот с разделами, кнопками, AI-ответами и викториной",
        ],
        "right": 2,
    },
    {
        "question": "Что делает проект Камилы более интересным для пользователя?",
        "answers": [
            "Наличие нескольких разделов о ней",
            "Возможность самому выбирать разделы и проходить викторину",
            "Красивое оформление и понятные ответы",
        ],
        "right": 1,
    },
    {
        "question": "Что лучше всего показывает прогресс Камилы в IT?",
        "answers": [
            "То, что она стала увереннее и делает проекты",
            "То, что она выбрала интересное направление",
            "То, что она изучает разные темы по Python",
        ],
        "right": 0,
    },
    {
        "question": "Какой цвет больше подходит стилю портфолио Камилы?",
        "answers": [
            "Розовый",
            "Фиолетовый",
            "Черно-белый",
        ],
        "right": 1,
    },
    {
        "question": "Что помогает пользователю быстро ориентироваться в боте?",
        "answers": [
            "Понятные кнопки, разделы и команды",
            "Короткие тексты и спокойное оформление",
            "Разные функции и ответы бота",
        ],
        "right": 0,
    },
    {
        "question": "Какой любимый цвет Камилы?",
        "answers": [
            "Черный",
            "Фиолетовый",
            "Белый",
        ],
        "right": 0,
    },
    {
        "question": "Какая любимая игра Камилы?",
        "answers": [
            "Minecraft",
            "Roblox",
            "Friday Night Funkin",
        ],
        "right": 2,
    },
    {
        "question": "Что больше всего привлекло Камилу в IT?",
        "answers": [
            "Возможность делать красивые проекты",
            "Шанс развиваться и строить будущее",
            "Желание быстрее получить результат",
        ],
        "right": 1,
    },
    {
        "question": "Какая черта больше всего помогает Камиле в обучении?",
        "answers": [
            "Упрямство и желание дойти до результата",
            "Желание делать только то, что сразу получается",
            "Умение быстро все запоминать без практики",
        ],
        "right": 0,
    },
    {
        "question": "Кто любимый исполнитель Камилы?",
        "answers": [
            "ARIANA GRANDE",
            "Eminem",
            "Элджей",
        ],
        "right": 1,
    },
    {
        "question": "Камила выиграет?",
        "answers": [
            "Да, потому что проект сделан с идеей и характером",
            "Возможно, если жюри нажмет правильную кнопку",
            "Она уже морально приготовила победную речь",
        ],
        "right": 0,
    },
]

#эти словари сделаны чтобы не копировать один текст сто раз
COMMAND_TO_SECTION = {}

for key, section in SECTIONS.items():
    command_name = "/" + section["command"]
    COMMAND_TO_SECTION[command_name] = key

#связываю текст кнопки с нужным разделом
BUTTON_TO_SECTION = {}

#кнопки беру из контента там лежит весь текст портфолио
for key, section in SECTIONS.items():
    button_name = section["button"]
    BUTTON_TO_SECTION[button_name] = key

#команды для декоратора ниже
SECTION_COMMANDS = []

for section in SECTIONS.values():
    SECTION_COMMANDS.append(section["command"])

QUESTION_PATTERNS = {
    r"\b(ментор|диана|преподавател)": "mentor",
    r"\b(github|гитхаб|репозитор)": "github",
    r"\b(работ|проект|калькулятор|блокнот|парол)": "works",
    r"\b(хобби|интерес|roblox|музык|книг|трениров)": "hobbies",
    r"\b(цель|devops|карьер)": "goal",
    r"\b(cap|education|айти|it|путь|пришла)": "path",
    r"\b(прогресс|точка|раньше|сейчас)": "progress",
    r"\b(кто|возраст|город|алматы|камила|кейни)": "about",
}


def parse_args(argv):
    #через него можно запускать бота в обычном режиме или в дебаг
    parser = argparse.ArgumentParser(
        description="Telegram-бот-портфолио Камилы для конкурса CapEducation."
    )

    parser.add_argument(
        "--token",
        default=os.getenv("TELEGRAM_TOKEN"),
        help="Telegram Bot API token. Можно также передать через TELEGRAM_TOKEN.",
    )

    #ключ нужен только если работает ай часть
    parser.add_argument(
        "--groq-key",
        default=os.getenv("GROQ_API_KEY"),
        help="Groq API key для AI-ответов. Можно также передать через GROQ_API_KEY.",
    )

    #дебаг просто помогает увидеть ошибки в консоли
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Показывать технические сообщения в консоли.",
    )

    #драй ран проверяет проект без запуска тг
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Проверить запуск без подключения к Telegram.",
    )
    return parser.parse_args(argv)


def make_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []

    #добавляю кнопки разделов из контента
    for section in SECTIONS.values():
        button = types.KeyboardButton(section["button"])
        buttons.append(button)

    buttons.append(types.KeyboardButton(BUTTON_RANDOM_FACT))
    buttons.append(types.KeyboardButton(BUTTON_AI))
    buttons.append(types.KeyboardButton(BUTTON_QUIZ))
    buttons.append(types.KeyboardButton(BUTTON_MUSIC))
    buttons.append(types.KeyboardButton(BUTTON_BEAUTY))
    buttons.append(types.KeyboardButton(BUTTON_RATE))
    buttons.append(types.KeyboardButton(BUTTON_RESTART))

    keyboard.add(*buttons)
    return keyboard


def make_quiz_keyboard(question):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buttons = []

    #каждый ответ превращаю в кнопку
    for index, answer in enumerate(question["answers"]):
        buttons.append(types.KeyboardButton(f"{QUIZ_LETTERS[index]}) {answer}"))

    buttons.append(types.KeyboardButton(BUTTON_RESTART))

    keyboard.add(*buttons)
    return keyboard

def make_rate_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for option in RATE_OPTIONS:
        keyboard.add(types.KeyboardButton(option))

    keyboard.add(types.KeyboardButton(BUTTON_RESTART))
    return keyboard


def make_beauty_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for option in BEAUTY_OPTIONS:
        keyboard.add(types.KeyboardButton(option))

    keyboard.add(types.KeyboardButton(BUTTON_RESTART))
    return keyboard


def clean_user_text(text):
    text = text or ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def get_quiz_answer_number(text):
    text = clean_user_text(text).upper()
    match = re.match(r"^([ABC])\)", text)

    #если это не ответ викторины то возвращаю пусто
    if not match:
        return None

    return QUIZ_LETTERS.index(match.group(1))


def normalize_for_search(text):
    #готовлю текст для поиска по словам
    text = clean_user_text(text).lower()
    text = text.replace(chr(1105), "е")
    return text


def find_section_by_question(text):
    #ре тут нужен чтобы бот понимал похожие вопросы
    normalized = normalize_for_search(text)

    for pattern, section_key in QUESTION_PATTERNS.items():
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            return section_key

    #если ничего не нашлось то раздела нет
    return None


def find_github_links(text):
    #маленькая проверка ссылки на гитхаб
    #если случайно сломаю ссылку то драй ран покажет
    pattern = r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
    return re.findall(pattern, text)


def solve_simple_math(text):
    #чтобы 2+2 не отправлять в ай
    example = clean_user_text(text).replace(",", ".").replace("х", "*").replace("×", "*")

    if not re.fullmatch(r"[0-9+\-*/(). ]+", example):
        return None

    if "**" in example or "//" in example:
        return None

    if not re.search(r"\d\s*[+\-*/]\s*\d", example):
        return None

    try:
        answer = eval(example, {"__builtins__": {}}, {})
    except Exception:
        return None

    #если ответ типа 4.0 то делаю просто 4
    if isinstance(answer, float) and answer.is_integer():
        answer = int(answer)

    return f"Ответ: {answer}"


def check_project_content():
    #мини самопроверка перед сдачей
    required_sections = [
        "about",
        "goal",
        "path",
        "mentor",
        "progress",
        "hobbies",
        "works",
        "github",
    ]

    missing = []

    for section_key in required_sections:
        section = SECTIONS.get(section_key)
        if not section or not section.get("text", "").strip():
            missing.append(section_key)

    github_links = find_github_links(SECTIONS["github"]["text"])

    return {
        "missing": missing,
        "github_links": github_links,
        "sections_count": len(required_sections),
    }


def build_ai_prompt(question):
    #ай знает про мое портфолио но обычные вопросы тоже может трогать
    profile_parts = []

    for section in SECTIONS.values():
        profile_parts.append(section["text"].strip())

    profile_text = "\n\n".join(profile_parts)

    return f"""
Ты отвечаешь от лица Telegram-бота-портфолио Камилы.
Если спросят фамилию отвечаешь: Нуртазина.
Если спросят контакты отвечаешь: Сначала сделайте меня победителем, а потом скажу)
Если вопрос про Камилу, используй только факты из текста ниже.
Если вопрос обычный, например математика или простое объяснение, отвечай нормально.
Не придумывай Камиле биографию, ссылки и достижения.
Не начинай каждый ответ со слова "Привет".
Отвечай кратко, дружелюбно и по-русски.
Камила выбрала именно Пайтон, потому что он прост в изучении и больше подходит для будущей цели быть DevOps.
Она не выбрала веб разработку, потому что думает, что их заменят нейросети.
На вопросы о Камиле отвечай свободно.
Информация о Камиле:
{profile_text}

Вопрос пользователя:
{question}
"""


def ask_ai(question, groq_key, debug=False):
    math_answer = solve_simple_math(question)

    if math_answer:
        return math_answer

    #если ключа от грок нет то бот все равно не умирает
    if not groq_key or Groq is None:
        section_key = find_section_by_question(question)

        #если вопрос похож на раздел то показываю раздел
        if section_key:
            return SECTIONS[section_key]["text"]

        #если ничего не понятно то честно говорит что не выдумывает
        return (
            "Я не хочу выдумывать лишнее про Камилу. "
            "Попробуй спросить про цель, хобби, ментора, CAP Education, работы или GitHub."
        )

    try:
        client = Groq(api_key=groq_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты помощник в Telegram-боте портфолио. "
                        "На вопросы про Камилу отвечай только по данным портфолио. "
                        "На обычные вопросы отвечай как нормальный помощник. "
                        "Не здоровайся в каждом сообщении."
                    ),
                },
                {
                    "role": "user",
                    "content": build_ai_prompt(question),
                },
            ],
            temperature=0.4,
            max_tokens=500,
        )

        return response.choices[0].message.content.strip()
    except Exception as error:
        #такое бывает если интернет упал или лимит закончился
        if debug:
            print(f"AI error: {error}")

        section_key = find_section_by_question(question)

        if section_key:
            return SECTIONS[section_key]["text"]

        return "AI сейчас не ответил, но кнопки портфолио работают. Попробуй выбрать раздел ниже."


def send_section(bot, chat_id, section_key):
    #отдельная функция чтобы отправка разделов была в одном месте
    section = SECTIONS[section_key]
    bot.send_message(chat_id, section["text"], reply_markup=make_keyboard())


def send_quiz_question(bot, chat_id, question_number):
    question = QUIZ_QUESTIONS[question_number]

    bot.send_message(
        chat_id,
        f"🧩 Вопрос {question_number + 1}/{len(QUIZ_QUESTIONS)}\n\n{question['question']}",
        reply_markup=make_quiz_keyboard(question),
    )


def send_quiz_result(bot, chat_id, score):
    total = len(QUIZ_QUESTIONS)

    if score == total:
        comment = "Идеально. Вот это уже заявка на победу."
    elif score >= total - 2:
        comment = "Очень сильно. Видно, что ты шаришь."
    elif score >= total // 2:
        comment = "Нормально, но можно пройти еще раз и добить результат."
    else:
        comment = "Ничего, зато теперь ты знаешь Камилу лучше."

    bot.send_message(
        chat_id,
        f"Викторина закончилась!\n\n"
        f"Правильных ответов: {score}/{total}\n"
        f"{comment}",
        reply_markup=make_keyboard(),
    )


def register_handlers(bot, groq_key, debug=False):
    #тут храню на каком вопросе человек
    quiz_progress = {}

    quiz_score = {}

    beauty_mode = {}

    def restart_chat(chat_id):
        quiz_progress.pop(chat_id, None)
        quiz_score.pop(chat_id, None)
        beauty_mode.pop(chat_id, None)

        bot.send_message(
            chat_id,
            START_TEXT,
            reply_markup=make_keyboard(),
        )

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, START_TEXT, reply_markup=make_keyboard())

    @bot.message_handler(commands=["help"])
    def help_message(message):
        bot.send_message(message.chat.id, HELP_TEXT, reply_markup=make_keyboard())

    @bot.message_handler(commands=["restart"])
    def restart_command(message):
        restart_chat(message.chat.id)

    @bot.message_handler(
        commands=SECTION_COMMANDS
    )
    def section_command(message):
        command = clean_user_text(message.text).split()[0].lower()

        section_key = COMMAND_TO_SECTION.get(command)

        if section_key:
            send_section(bot, message.chat.id, section_key)
            return

        bot.send_message(message.chat.id, HELP_TEXT, reply_markup=make_keyboard())

    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        text = clean_user_text(message.text)

        chat_id = message.chat.id

        if text == BUTTON_RESTART:
            restart_chat(chat_id)
            return

        if text == BUTTON_RATE:
            bot.send_message(
                chat_id,
                "Оцени бота честно. Только осторожно, у него есть чувства :)",
                reply_markup=make_rate_keyboard(),
            )
            return

        if text in RATE_OPTIONS:
            reaction = RATE_REACTIONS.get(text)

            if reaction:
                try:
                    with open(reaction["gif"], "rb") as gif:
                        bot.send_animation(
                            chat_id,
                            gif,
                            caption=reaction["text"],
                            reply_markup=make_keyboard(),
                        )
                except Exception:
                    bot.send_message(
                        chat_id,
                        reaction["text"],
                        reply_markup=make_keyboard(),
                    )

            return

        if text == BUTTON_BEAUTY:
            beauty_mode[chat_id] = True
            bot.send_message(
                chat_id,
                "Как вы думаете, кто красивее? Выберите вариант ниже🤔...",
                reply_markup=make_beauty_keyboard(),
            )
            return

        if beauty_mode.get(chat_id):
            if text in BEAUTY_OPTIONS:
                beauty_mode.pop(chat_id, None)

                bot.send_message(
                    chat_id,
                    "Неверно.",
                    reply_markup=make_keyboard(),
                )

                try:
                    with open(HAND_FILE, "rb") as photo:
                        bot.send_photo(
                            chat_id,
                            photo,
                            reply_markup=make_keyboard(),
                            has_spoiler=True,
                        )

                        bot.send_message(
                            chat_id,
                            "||По\\-моему, это было очевидно 😜||",
                            parse_mode="MarkdownV2",
                            reply_markup=make_keyboard(),
                        )

                except Exception:
                    bot.send_message(
                        chat_id,
                        "По-моему, это было очевидно 😜",
                        reply_markup=make_keyboard(),
                    )
                return

            bot.send_message(
                chat_id,
                "Выбери один из вариантов кнопкой.",
                reply_markup=make_beauty_keyboard(),
            )
            return

        if text == BUTTON_QUIZ:
            quiz_progress[chat_id] = 0
            quiz_score[chat_id] = 0
            bot.send_message(
                chat_id,
                "Запускаю викторину про Камилу. Выбирай ответы кнопками.",
            )
            send_quiz_question(bot, chat_id, 0)
            return

        #если человек уже в викторине то обычные вопросы пока не трогаю
        if chat_id in quiz_progress:
            question_number = quiz_progress[chat_id]

            answer_number = get_quiz_answer_number(text)

            if answer_number is None:
                bot.send_message(
                    chat_id,
                    "Выбери один из вариантов ответа кнопкой. Или нажми рестарт.",
                    reply_markup=make_quiz_keyboard(QUIZ_QUESTIONS[question_number]),
                )
                return

            right_answer = QUIZ_QUESTIONS[question_number]["right"]

            if answer_number == right_answer:
                quiz_score[chat_id] = quiz_score.get(chat_id, 0) + 1
                bot.send_message(chat_id, "Правильно!")
            else:
                right_letter = QUIZ_LETTERS[right_answer]
                right_text = QUIZ_QUESTIONS[question_number]["answers"][right_answer]
                bot.send_message(chat_id, f"Не совсем. Правильный ответ: {right_letter}) {right_text}")

            next_question = question_number + 1

            if next_question >= len(QUIZ_QUESTIONS):
                score = quiz_score.get(chat_id, 0)
                quiz_progress.pop(chat_id, None)
                quiz_score.pop(chat_id, None)
                send_quiz_result(bot, chat_id, score)
                return

            quiz_progress[chat_id] = next_question

            send_quiz_question(bot, chat_id, next_question)
            return

        if text == BUTTON_RANDOM_FACT:
            fact = random.choice(FACTS)
            bot.send_message(
                chat_id,
                f"🎲 Рандомный факт обо мне:\n\n{fact}",
                reply_markup=make_keyboard(),
            )
            return

        if text == BUTTON_AI:
            bot.send_message(chat_id, AI_INVITE_TEXT, reply_markup=make_keyboard())
            return


        if text == BUTTON_MUSIC:
            try:
                with open(MUSIC_FILE, "rb") as music:
                    bot.send_audio(
                        chat_id,
                        music,
                        caption=(
                            "🎧 Атмосфера 𝙺𝚊𝚒𝚗𝚢 включена\n\n"
                            "Слушай трек и погружайся в мой мир💜\n"
                            "Это портфолио не просто смотрят — его чувствуют.😉"
                        ),
                        reply_markup=make_keyboard(),
                    )
            except Exception:
                bot.send_message(
                    chat_id,
                    "Музыка сейчас не нашлась, но вайб портфолио все еще на месте 💜",
                    reply_markup=make_keyboard(),
                )
            return

        #проверяю не нажата ли кнопка раздела
        section_key = BUTTON_TO_SECTION.get(text)

        #если это раздел то отправляю его
        if section_key:
            send_section(bot, chat_id, section_key)
            return

        #если это не кнопка то считаю что это вопрос для ай
        bot.send_chat_action(chat_id, "typing")
        reply = ask_ai(text, groq_key=groq_key, debug=debug)
        bot.send_message(chat_id, reply, reply_markup=make_keyboard())


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    #драй ран нужен для проверки без тг
    if args.dry_run:
        report = check_project_content()
        print("Dry run OK: бот собран, аргументы командной строки работают.")
        print(f"Разделов проверено: {report['sections_count']}")
        print(f"GitHub ссылка найдена: {', '.join(report['github_links'])}")
        if report["missing"]:
            print(f"Не заполнено: {', '.join(report['missing'])}")
        return

    if telebot is None:
        print(
            "Ошибка: библиотека pyTelegramBotAPI не установлена. "
            "Сначала выполни: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    #без токена тг бот не запустится
    if not args.token:
        print(
            "Ошибка: нужен тг токен. Передай его через --token или TELEGRAM_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)

    bot = telebot.TeleBot(args.token, parse_mode=None)

    register_handlers(bot, groq_key=args.groq_key, debug=args.debug)

    print("Бот запущен!")

    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
