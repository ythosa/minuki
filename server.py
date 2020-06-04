# The telegram bot server that runs directly

from aiogram import Bot, Dispatcher, executor, types
import logging

import expenses
from exceptions import NotCorrectMessage, NotCorrectExpenseIDToDelete
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


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Sends a list of expense categories"""
    categories = expenses.Categories().get_all_categories()
    answer_message = "Categories of expenses:\n\n* " + \
                     "\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories])
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def expenses_list(message: types.Message):
    """Sends the last few records on the costs"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Expenses haven't been set up yet")
        return

    last_expenses_row = [
        f"{expense.amount} rub. of {expense.category_name} — press "
        f"/del{expense.id} for removal"
        for expense in last_expenses
    ]

    answer_message = "Last saved expenses:\n\n* " + "\n\n* ".join(last_expenses_row)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def delete_expense(message: types.Message):
    """Deletes a single expense record by its ID"""
    row_id = int(message.text[4:])

    try:
        expenses.delete_expense(row_id)
    except NotCorrectExpenseIDToDelete as e:
        await message.answer(str(e))
        return

    await message.answer("Removed 👌")


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Sends today's spending statistics"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Sends spending statistics for the current month"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Adds new expense"""
    try:
        expense = expenses.add_expense(message.text)
    except NotCorrectMessage as e:
        await message.answer(str(e))
        return

    answer_message = (
        f"Added expenses {expense.amount} rub on {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}"
    )

    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
