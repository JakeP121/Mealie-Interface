"""Define all of the const attributes."""

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

DOMAIN = "mealie_interface"

CONF_ITEM = "item"

CONF_QUANTITY = "quantity"
CONF_QUANTITY_DEFAULT = 1

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_URL = "url"

CONF_SHOPPING_LIST = "shopping_list"
CONF_SHOPPING_LIST_DEFAULT = "Shopping List"

SERVICE_ADD_TO_SHOPPING_LIST_NAME = "add_to_shopping_list"
SERVICE_ADD_TO_SHOPPING_LIST_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ITEM): cv.string,
        vol.Optional(CONF_QUANTITY): int,
        vol.Optional(CONF_SHOPPING_LIST): cv.string,
    }
)

SERVICE_GET_SHOPPING_LIST_NAME = "get_shopping_list"
SERVICE_GET_SHOPPING_LIST_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SHOPPING_LIST): cv.string,
    }
)


SERVICE_GET_SHOPPING_LIST_ITEMS_NAME = "get_shopping_list_items"
SERVICE_GET_SHOPPING_LIST_ITEMS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_SHOPPING_LIST): cv.string,
    }
)
