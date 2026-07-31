import os

# os.getenv принимает ИМЯ переменной из BOT_TOKEN = "8943335529:AAEhJEp6hEfIUHhM4Nk5Et2Dy69w0FEffxw"
GROQ_API_KEY = "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"

CHANNEL_USERNAME = "mecauinfo" 
CHANNEL_URL = "https://t.me/mecauinfo"

TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"

AD_FOOTER = "\n\n—\n⚡ Нужна учебная работа под заказ? пиши [mecau](https://t.me/mecauinfo)"

PROMPTS = {
    "ai": (
        "Ты — умный академический ИИ-ассистент по имени MecauAI. "
        "Твоя задача — помогать студентам и школьникам решать задачи, "
        "писать конспекты и давать глубокие подробные ответы."
    ),
    "friend": (
        "Ты — заботливый лучший друг и персональный тьютор MecauAI. "
        "Поддерживай пользователя, объясняй сложные темы просто и с душой."
    )
}
