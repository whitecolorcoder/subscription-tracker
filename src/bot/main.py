from aiogram import Dispatcher, Bot
from aiogram.types import Message
import asyncio
import os
from dotenv import load_dotenv
import httpx
from aiogram.utils.serialization import deserialize_telegram_object_to_python
import json
from aiogram.types import Message

load_dotenv()

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError("Токен не найден в переменных окружения!")

bot = Bot(token= TOKEN)
dp = Dispatcher()


@dp.message()
async def cmd_message(message: Message):
    await message.answer("Hi!")

    raw_dict = deserialize_telegram_object_to_python(message)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/webhook",
            json=raw_dict
        )

    print(response.status_code)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

