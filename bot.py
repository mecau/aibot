import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from docxtpl import DocxTemplate

# ----------------- НАСТРОЙКИ -----------------
BOT_TOKEN = "8943335529:AAEhJEp6hEfIUHhM4Nk5Et2Dy69w0FEffxw"
CHANNEL_ID = "@твой_канал"  # Вставь юзернейм своего инфо-канала с собачкой (например, @my_channel)
CHANNEL_LINK = "https://t.me/твой_канал"  # Вставь ссылку на канал
MY_USERNAME = "@mecau"  # Твой контакты для заказов

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----------------- FSM (СОСТОЯНИЯ) -----------------
class TitleForm(StatesGroup):
    vuz = State()
    work_type = State()
    theme = State()
    student = State()
    teacher = State()

# ----------------- КЛАВИАТУРЫ -----------------
def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
    ])

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Сгенерировать титульник (ГОСТ)", callback_data="make_title")],
        [InlineKeyboardButton(text="💡 Заказать работу под ключ", url=f"https://t.me/{MY_USERNAME.replace('@', '')}")]
    ])

# ----------------- ПРОВЕРКА ПОДПИСКИ -----------------
async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        # Если канал еще не настроен, временно пускает всех
        return True

# ----------------- ХЭНДЛЕРЫ -----------------
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if not await is_subscribed(message.from_user.id):
        await message.answer(
            "🔒 **Доступ ограничен!**\n\nДля использования бота подпишись на наш инфо-канал.",
            reply_markup=sub_keyboard(),
            parse_mode="Markdown"
        )
        return
    
    await message.answer(
        "👋 Привет! Я помогу тебе быстро сформировать правильный титульный лист по ГОСТу.\n\nВыбери действие ниже:", 
        reply_markup=main_keyboard()
    )

@dp.callback_query(F.data == "check_sub")
async def check_sub_handler(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text("✅ Отлично! Доступ открыт. Выбери нужную функцию:", reply_markup=main_keyboard())
    else:
        await callback.answer("❌ Вы всё ещё не подписаны на канал!", show_alert=True)

# --- ГЕНЕРАЦИЯ ТИТУЛЬНИКА ---
@dp.callback_query(F.data == "make_title")
async def start_title(callback: types.CallbackQuery, state: FSMContext):
    if not await is_subscribed(callback.from_user.id):
        await callback.message.answer("Подпишись на канал, чтобы использовать бота!", reply_markup=sub_keyboard())
        return
    
    await state.set_state(TitleForm.vuz)
    await callback.message.answer("Шаг 1/5: Введи название твоего ВУЗа (например: МГУ им. М.В. Ломоносова):")

@dp.message(TitleForm.vuz)
async def process_vuz(message: types.Message, state: FSMContext):
    await state.update_data(vuz=message.text)
    await state.set_state(TitleForm.work_type)
    await message.answer("Шаг 2/5: Укажи тип работы (например: Курсовая работа, Дипломная работа, Реферат):")

@dp.message(TitleForm.work_type)
async def process_type(message: types.Message, state: FSMContext):
    await state.update_data(work_type=message.text)
    await state.set_state(TitleForm.theme)
    await message.answer("Шаг 3/5: Введи тему работы:")

@dp.message(TitleForm.theme)
async def process_theme(message: types.Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await state.set_state(TitleForm.student)
    await message.answer("Шаг 4/5: Введи ФИО студента и курс/группу (например: Иванов И. И., 3 курс):")

@dp.message(TitleForm.student)
async def process_student(message: types.Message, state: FSMContext):
    await state.update_data(student=message.text)
    await state.set_state(TitleForm.teacher)
    await message.answer("Шаг 5/5: Введи ФИО и звание преподавателя (например: проф. Петров П. П.):")

@dp.message(TitleForm.teacher)
async def process_teacher(message: types.Message, state: FSMContext):
    await state.update_data(teacher=message.text)
    data = await state.get_data()
    await state.clear()

    msg = await message.answer("⏳ Генерирую документ по ГОСТу...")

    try:
        doc = DocxTemplate("template.docx")
        context = {
            'vuz': data['vuz'],
            'type': data['work_type'],
            'theme': data['theme'],
            'student': data['student'],
            'teacher': data['teacher'],
            'year': "2026"
        }
        
        filename = f"титульник_{message.from_user.id}.docx"
        doc.render(context)
        doc.save(filename)

        file_to_send = FSInputFile(filename)
        await message.answer_document(
            file_to_send,
            caption=f"✅ **Твой титульный лист готов!**\n\n💡 *Горят дедлайны или нужна помощь с написанием всей работы под ключ? Напиши {MY_USERNAME} — сделаем быстро и с гарантией Антиплагиата!*",
            parse_mode="Markdown"
        )
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Произошла ошибка при сборке файла. Убедись, что template.docx загружен верно.")

# ----------------- ЗАПУСК -----------------
async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
