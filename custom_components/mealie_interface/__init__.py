"""A custom component to provide an interface to Mealie through Home Assistant services."""

import logging

from homeassistant.core import SupportsResponse

from .const import (
    CONF_ITEM,
    CONF_PASSWORD,
    CONF_QUANTITY,
    CONF_QUANTITY_DEFAULT,
    CONF_SHOPPING_LIST,
    CONF_SHOPPING_LIST_DEFAULT,
    CONF_URL,
    CONF_USERNAME,
    DOMAIN,
    SERVICE_ADD_TO_SHOPPING_LIST_NAME,
    SERVICE_ADD_TO_SHOPPING_LIST_SCHEMA,
    SERVICE_GET_SHOPPING_LIST_ITEMS_NAME,
    SERVICE_GET_SHOPPING_LIST_ITEMS_SCHEMA,
    SERVICE_GET_SHOPPING_LIST_NAME,
    SERVICE_GET_SHOPPING_LIST_SCHEMA,
)
from .Mealie import Exceptions, Mealie

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    username = config[DOMAIN][CONF_USERNAME]
    password = config[DOMAIN][CONF_PASSWORD]
    api_url = config[DOMAIN][CONF_URL] + "/api"

    def set_state(entity_name, state):
        """Set an entity's state."""
        hass.states.set(DOMAIN + "." + entity_name, state)

    #
    # Add to Shopping List
    #
    def service_add_to_shopping_list(call):
        """Handle the add_to_shopping_list service call."""
        item_name = call.data.get(CONF_ITEM)
        quantity = call.data.get(CONF_QUANTITY, CONF_QUANTITY_DEFAULT)
        shopping_list_name = call.data.get(
            CONF_SHOPPING_LIST, CONF_SHOPPING_LIST_DEFAULT
        )

        mealie = Mealie.Mealie(api_url, username, password)
        response_item = None
        try:
            response_item = mealie.find_and_add_to_shopping_list(
                item_name, quantity, shopping_list_name
            )
        except Exceptions.MealieException as exc:
            exc.log_exception()
            return {"success": False, "response": str(exc)}

        if response_item is None:
            return {
                "success": False,
                "response": "Unknown exception: find_and_add_to_shopping_list didn't raise an exception but also didn't return an Item",
            }

        return {
            "success": True,
            "response": "Added to shopping list",
            "item": response_item,
            "shopping_list": shopping_list_name,
        }

    hass.services.register(
        domain=DOMAIN,
        service=SERVICE_ADD_TO_SHOPPING_LIST_NAME,
        service_func=service_add_to_shopping_list,
        schema=SERVICE_ADD_TO_SHOPPING_LIST_SCHEMA,
        supports_response=SupportsResponse.OPTIONAL,
    )

    #
    # Get Shopping List
    #
    def service_get_shopping_list(call):
        """Handle the get_shopping_list service call."""
        shopping_list_name = call.data.get(
            CONF_SHOPPING_LIST, CONF_SHOPPING_LIST_DEFAULT
        )

        mealie = Mealie.Mealie(api_url, username, password)
        response_shopping_list = None
        try:
            response_shopping_list = mealie.get_shopping_list(shopping_list_name)
        except Exceptions.MealieException as exc:
            exc.log_exception()
            return {"success": False, "response": str(exc)}

        if response_shopping_list is None:
            return {
                "success": False,
                "response": "Unknown exception: get_shopping_list didn't raise an exception but also didn't return a Shopping List",
            }

        return {
            "success": True,
            "response": "Found shopping list",
            "shopping_list": response_shopping_list,
        }

    hass.services.register(
        domain=DOMAIN,
        service=SERVICE_GET_SHOPPING_LIST_NAME,
        service_func=service_get_shopping_list,
        schema=SERVICE_GET_SHOPPING_LIST_SCHEMA,
        supports_response=SupportsResponse.OPTIONAL,
    )

    #
    # Get Shopping List Items
    #
    def service_get_shopping_list_items(call):
        """Handle the get_shopping_list_items service call."""
        shopping_list_name = call.data.get(
            CONF_SHOPPING_LIST, CONF_SHOPPING_LIST_DEFAULT
        )

        mealie = Mealie.Mealie(api_url, username, password)
        try:
            shopping_list = mealie.get_shopping_list_items(shopping_list_name)
            response_items = mealie.get_shopping_list_items(shopping_list)
        except Exceptions.MealieException as exc:
            exc.log_exception()
            return {"success": False, "response": str(exc)}

        return {
            "success": True,
            "response": "Found shopping list",
            "shopping_list": shopping_list_name,
            "items": response_items,
        }

    hass.services.register(
        domain=DOMAIN,
        service=SERVICE_GET_SHOPPING_LIST_ITEMS_NAME,
        service_func=service_get_shopping_list_items,
        schema=SERVICE_GET_SHOPPING_LIST_ITEMS_SCHEMA,
        supports_response=SupportsResponse.OPTIONAL,
    )
    # Return boolean to indicate that initialization was successful.
    return True
