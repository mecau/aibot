import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


CHANNEL_USERNAME = "mecauinfo" 
CHANNEL_URL = "https://t.me/mecauinfo"

TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"

AD_FOOTER = "\n\n—\n⚡ Нужна учебная работа под заказ? пиши @mecau"

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
