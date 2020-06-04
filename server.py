# The telegram bot server that runs directly

from aiogram import Bot, Dispatcher, executor, types
import logging

from middlewares import AccessMiddleware
from tokens import API_TOKEN, ACCESS_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends a welcome message and help on the bot"""
    await message.answer(
        "Bot for accounting for finances\n\n"
        "Add expense: 250 taxis\n"
        "Today's statistics: /today\n"
        "For current month: /month\n"
        "Last expenses paid: /expenses\n"
        "Categories of expenses: /categories")


# @dp.message_handler()
# async def add_expense(message: types.Message):
#     """Adds new expense"""
#     try:
#         expense =


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
