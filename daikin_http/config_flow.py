"""Handles the config flow for Daikin HTTP integration."""

from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, CONF_HOST


class DaikinHttpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Daikin HTTP."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where user inputs data."""
        errors = {}

        if user_input is not None:
            # Create config entry with user data
            return self.async_create_entry(title="Daikin HTTP AC", data=user_input)

        # Show the config form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                }
            ),
            errors=errors,
        )
