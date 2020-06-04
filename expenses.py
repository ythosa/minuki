import re
from typing import NamedTuple, Optional

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
