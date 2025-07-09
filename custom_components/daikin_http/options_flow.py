import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN


class DaikinHttpOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Daikin HTTP."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "name",
                        default=self.config_entry.options.get(
                            "name", self.config_entry.data.get("name", "Daikin HTTP AC")
                        ),
                    ): str,
                }
            ),
        )


@callback
def async_get_options_flow(config_entry):
    return DaikinHttpOptionsFlowHandler(config_entry)
