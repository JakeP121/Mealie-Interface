"""Interface for the Mealie API."""

import json

import requests

from ..REST.API import APIHandler
from .Exceptions import AlreadyExists, CouldNotFind, InvalidQuery


class Mealie(APIHandler):
    """Interface for the Mealie API."""

    def __init__(self, url: str, username: str, password: str) -> None:
        """Init."""
        super().__init__(url)
        self.username = username
        self.bearer_token = self.login(password=password)

    def login(self, password: str) -> bool:
        """Login to get the bearer token."""
        url = self.base_url + "/auth/token"
        data = {
            "username": self.username,
            "password": password,
        }

        response = requests.post(url, data=data, timeout=5)
        self.check_response(response)
        return response.json()["access_token"]

    def get_authorised_header(self):
        """Create a header dict that includes our authorised bearer token."""
        return {"Authorization": "Bearer " + self.bearer_token}

    def find_and_add_to_shopping_list(
        self, item_name: str, shopping_list, quantity: int = 1
    ):
        """Find an item and add it to the shopping list."""
        # Ignore if the item already exists in the shopping list (disabled since I added quantity)
        ignore_if_exists: bool = False
        if ignore_if_exists:
            existing_items = self.get_shopping_list_items(shopping_list["id"])
            for item in existing_items:
                if item_name.lower() == item["food"]["name"].lower():
                    raise AlreadyExists(
                        error_string="Shopping list already contains " + item_name
                    )

        item = self.get_item(item_name)
        self.add_item_to_shopping_list(item, quantity, shopping_list)

        shopping_list_items = self.get_shopping_list_items(shopping_list["id"])
        for shopping_list_item in shopping_list_items:
            if item_name.lower() == shopping_list_item["food"]["name"].lower():
                return shopping_list_item

        raise CouldNotFind(object_name=item_name)  # We should've added the item

    def get_shopping_list(self, shopping_list_name: str):
        """Get a shopping list object."""
        url = self.construct_endpoint_url("groups/shopping/lists")

        response = requests.get(url, headers=self.get_authorised_header(), timeout=10)
        self.check_response(response)
        if response.json()["total"] <= 0:
            raise InvalidQuery(response.status_code, url)

        mealie_shopping_lists = response.json()["items"]
        possibilities = []
        for mealie_shopping_list in mealie_shopping_lists:
            mealie_shopping_list_name = mealie_shopping_list["name"].lower()
            if shopping_list_name.lower() == mealie_shopping_list_name:
                return mealie_shopping_list
            else:
                possibilities.append(mealie_shopping_list_name)

        raise CouldNotFind(object_name=shopping_list_name, possibilities=possibilities)

    def get_shopping_list_items(
        self,
        shopping_list_id: str,
        ignore_completed: bool = True,
    ):
        """Get items in a shopping list."""
        url = self.construct_endpoint_url("groups/shopping/items")

        response = requests.get(url, headers=self.get_authorised_header(), timeout=10)
        self.check_response(response)

        mealie_items = response.json()["items"]
        return [
            item
            for item in mealie_items
            if (not ignore_completed) or (not item["checked"])
        ]

    def get_item(self, item_name: str) -> str:
        """Search for a food."""
        url = self.construct_endpoint_url(
            "foods",
            url_params={
                "search": item_name,
            },
        )

        response = requests.get(url, headers=self.get_authorised_header(), timeout=10)
        self.check_response(response)
        if response.json()["total"] <= 0:
            raise CouldNotFind(object_name=item_name)

        mealie_items = response.json()["items"]
        possibilities = []
        for mealie_item in mealie_items:
            mealie_item_name = mealie_item["name"].lower()
            if item_name.lower() == mealie_item_name:
                return mealie_item
            else:
                possibilities.append(mealie_item_name)

        raise CouldNotFind(object_name=item_name, possibilities=possibilities)

    def add_item_to_shopping_list(self, item, quantity, shopping_list):
        """Add an item to the shopping list."""
        url = self.construct_endpoint_url("groups/shopping/items")

        data = {
            "quantity": quantity,  # Omitted anyway
            "food": {
                "id": item["id"],
                "name": item["name"],
                "description": item["description"],
                "extras": item["extras"],
                "labelId": item["labelId"],
                "aliases": [],
                "label": item["label"],
                "createdAt": item["createdAt"],
                "updateAt": item["updateAt"],
            },
            "note": "",
            "isFood": True,
            "disableAmount": True,
            "display": item["name"],
            "shoppingListId": shopping_list["id"],
            "checked": False,
            "position": 0,
            "foodId": item["id"],
            "labelId": item["labelId"],
            "extras": {},
            "recipeReferences": [],
        }

        r = requests.post(
            url, data=json.dumps(data), headers=self.get_authorised_header(), timeout=10
        )
        self.check_response(r)

    def check_item_from_shopping_list(self, item):
        """Check an item to remove it from the shopping list."""
        url = self.construct_endpoint_url("groups/shopping/items/" + item["id"])

        data = item
        data["checked"] = True

        r = requests.put(
            url, data=json.dumps(data), headers=self.get_authorised_header(), timeout=10
        )
        self.check_response(r)
