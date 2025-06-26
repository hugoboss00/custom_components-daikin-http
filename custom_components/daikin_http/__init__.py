"""Initialize Daikin HTTP integration."""

from .coordinator import DaikinCoordinator
from .const import DOMAIN, CONF_HOST
from homeassistant.const import Platform


PLATFORMS = [Platform.CLIMATE]


async def async_setup_entry(hass, entry):
    """Set up Daikin HTTP using config entry."""
    host = entry.data[CONF_HOST]
    coordinator = DaikinCoordinator(hass, host)
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator for access by the climate platform
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    """Unload Daikin HTTP config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
