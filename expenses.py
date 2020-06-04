import datetime
import re
from typing import NamedTuple, Optional, List
import pytz

import db
from categories import Categories
import exceptions


class Message(NamedTuple):
    """Structure of a unpaired message about a new expense"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Structure of a new expense added to the database"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """Adds a new message. Accepts the text of the message that came to the bot as input."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)

    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })

    return Expense(
        id=None,
        amount=parsed_message.amount,
        category_name=category.name
    )


def last() -> List[Expense]:
    """Returns the last few expenses"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from expense e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10"
    )
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id: int) -> str:
    """Deletes a single expense record by its ID"""
    is_exist = False

    expenses = last()
    for expense in expenses:
        if expense.id == row_id:
            is_exist = True
            break

    if is_exist:
        db.delete("expense", row_id)
        return "Removed"
    else:
        return "Invalid command"


def get_today_statistics() -> str:
    """Returns a string of expense statistics for today"""
    cursor = db.get_cursor()
    cursor.execute(
        "select sum(amount)"
        "from expense where date(created)=date('now', 'localtime')"
    )
    result = cursor.fetchone()
    if not result[0]:
        return "Today there are no expenses yet"
    all_today_expenses = result[0]

    cursor.execute(
        "select sum(amount) "
        "from expense where date(created)=date('now', 'localtime') "
        "and category_codename in (select codename "
        "from category where is_base_expense=true)"
    )
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0

    return (
        f"Spending today:\n"
        f"Total — {all_today_expenses} rub\n"
        f"Base — {base_today_expenses} rub of {_get_budget_limit()} rub\n\n"
        f"For current month: /month"
    )


def get_month_statistics() -> str:
    """Returns a string of expense statistics for the current month"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'

    cursor = db.get_cursor()
    cursor.execute(
        f"select sum(amount) "
        f"from expense where date(created) >= '{first_day_of_month}'"
    )
    result = cursor.fetchone()
    if not result[0]:
        return 'There are no expenses yet this month'
    all_today_expenses = result[0]

    cursor.execute(
        f"select sum(amount) "
        f"from expense where date(created) >= '{first_day_of_month}' "
        f"and category_codename in (select codename "
        f"from category where is_base_expense=true)"
    )
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0

    return (
        f"Expenses in the current month:\n"
        f"Total — {all_today_expenses} rub\n"
        f"Base — {base_today_expenses} rub out of "
        f"{now.day * _get_budget_limit()} rub"
    )


def _parse_message(raw_message: str) -> Message:
    """Parses the text of the incoming message about the new expense."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "I can't understand the message. Write a message in the format, for example:\n\t1500 metro."
        )

    amount = int(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()

    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """Returns current date by string"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Returns the current datetime, taking into account the time zone of Moscow Time."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_budget_limit() -> int:
    """Returns the daily spending limit for basic basic spending"""
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]
