"""A custom component to provide an interface to Mealie through Home Assistant services."""

import logging

from homeassistant.core import SupportsResponse

from .const import (
    CONF_ITEM,
    CONF_NOTIFY_DEVICE,
    CONF_NOTIFY_DEVICE_DEFAULT,
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
    base_url = config[DOMAIN][CONF_URL]
    api_url = base_url + "/api"

    def set_state(entity_name, state):
        """Set an entity's state."""
        hass.states.set(DOMAIN + "." + entity_name, state)

    async def send_notification(entity_id, data):
        """Send a notification to a device."""
        await hass.services.async_call("notify", entity_id, data)

    #
    # Add to Shopping List
    #
    async def service_add_to_shopping_list(call):
        """Handle the add_to_shopping_list service call."""
        # Get input from service call
        item_name = call.data.get(CONF_ITEM)
        quantity = call.data.get(CONF_QUANTITY, CONF_QUANTITY_DEFAULT)
        shopping_list_name = call.data.get(
            CONF_SHOPPING_LIST, CONF_SHOPPING_LIST_DEFAULT
        )

        # Log into Mealie
        mealie = await hass.async_add_executor_job(
            Mealie.Mealie, api_url, username, password
        )

        response = None
        try:
            shopping_list = await hass.async_add_executor_job(
                mealie.get_shopping_list, shopping_list_name
            )

            mealie_item = await hass.async_add_executor_job(
                mealie.find_and_add_to_shopping_list,
                item_name,
                shopping_list,
                quantity,
            )

            response = {
                "success": True,
                "response": "Added " + item_name + " to your shopping list",
                "item": mealie_item,
                "shopping_list": shopping_list_name,
            }
        except Exceptions.MealieException as exc:
            exc.log_exception()
            response = {"success": False, "response": str(exc)}

        # Handle (optional) notification
        notify_device = call.data.get(CONF_NOTIFY_DEVICE, CONF_NOTIFY_DEVICE_DEFAULT)
        if notify_device is not None:
            try:
                shopping_list_url = base_url + "/shopping-lists/" + shopping_list["id"]
                await send_notification(
                    notify_device,
                    {
                        "title": "Mealie",
                        "message": response["response"],
                        "data": {
                            "url": shopping_list_url,
                            "clickAction": shopping_list_url,
                        },
                    },
                )
            except Exceptions.MealieException as exc:
                exc.log_exception()  # Non vital, just log it

        return response

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
            "response": "Here's your shopping list.",
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
            "response": "Here's what's on your shopping list.",
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
