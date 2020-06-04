# Work with categories
from typing import NamedTuple, List, Dict

import db


class Category(NamedTuple):
    """Structure of category"""
    codename: str
    name: str
    is_base_expanse: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        """Returns a reference list of expense categories from the database"""
        categories = db.fetchall(
            "category",
            "codename name is_base_expense aliases".split()
        )
        categories = self._fill_aliases(categories)

        return categories

    @staticmethod
    def _fill_aliases(categories: List[Dict]) -> List[Category]:
        """Fills in aliases for each category, i.e. possible
        names of this category that we can write in the message text.
        For example, the category "cafe" can be written as cafe,
        a restaurant and so on."""
        categories_result = []

        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))

            aliases.append(category["codename"])
            aliases.append(category["name"])

            categories_result.append(Category(
                codename=category["codename"],
                name=category["name"],
                is_base_expanse=category["is_base_expense"],
                aliases=aliases
            ))

        return categories_result

    def get_all_categories(self) -> List[Category]:
        """Returns reference of the categories"""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Returns a category by one of its aliases"""
        found = None
        other_category = None

        for category in self.get_all_categories():
            if category.codename == "others":
                other_category = category
            for aliases in category.aliases:
                if category_name in aliases:
                    found = category

        if not found:
            found = other_category

        return found
