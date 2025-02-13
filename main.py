import logging
import requests
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import API_TOKEN, WEATHER_API_KEY  # Импортируем токены из config.py

CITY_NAME = 'Брянск'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Команда /start
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    logging.info("Received /start command")
    await message.answer(
        "Привет! Я бот, который может предоставить прогноз погоды. Напиши /weather, чтобы получить прогноз.",
        parse_mode="HTML"
    )

# Команда /help
@router.message(Command(commands=['help']))
async def send_help(message: types.Message):
    logging.info("Received /help command")
    await message.answer(
        "Я могу помочь тебе с прогнозом погоды.\n\nКоманды:\n/start - Начать работу с ботом\n/help - Получить справку\n/weather - Получить прогноз погоды",
        parse_mode="HTML"
    )

# Команда /weather
@router.message(Command(commands=['weather']))
async def get_weather(message: types.Message):
    logging.info("Received /weather command")
    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric',
            timeout=10
        )
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        weather_info = f"Погода в {CITY_NAME}:\nТемпература: {temperature}°C\nОписание: {weather_description.capitalize()}"
        await message.answer(weather_info, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        await message.answer("Не удалось получить данные о погоде. Попробуйте позже.")

# Добавление маршрутизатора в диспетчер
dp.include_router(router)

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error starting polling: {e}")

if __name__ == '__main__':
    asyncio.run(main())
