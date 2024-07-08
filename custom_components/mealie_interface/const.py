"""Define all of the const attributes."""

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

DOMAIN = "mealie_interface"
VERSION = "0.2.0"

CONF_ITEM = "item"

CONF_QUANTITY = "quantity"
CONF_QUANTITY_DEFAULT = 1

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_URL = "url"

CONF_SHOPPING_LIST = "shopping_list"
CONF_SHOPPING_LIST_DEFAULT = "Shopping List"

CONF_NOTIFY_DEVICE = "notify_device"
CONF_NOTIFY_DEVICE_DEFAULT = None

SERVICE_ADD_TO_SHOPPING_LIST_NAME = "add_to_shopping_list"
SERVICE_ADD_TO_SHOPPING_LIST_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ITEM): cv.string,
        vol.Optional(CONF_QUANTITY): int,
        vol.Optional(CONF_SHOPPING_LIST): cv.string,
        vol.Optional(CONF_NOTIFY_DEVICE): cv.string,
    }
)

SERVICE_CHECK_FROM_SHOPPING_LIST_NAME = "check_from_shopping_list"
SERVICE_CHECK_FROM_SHOPPING_LIST_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ITEM): cv.string,
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
