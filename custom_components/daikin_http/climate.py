"""Platform for controlling a Daikin A/C via HTTP GET."""

import logging
import requests
# import aiohttp


from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)

from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE

from .const import DOMAIN, CONF_HOST

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = (
    ClimateEntityFeature.TURN_OFF
    | ClimateEntityFeature.TURN_ON
    | ClimateEntityFeature.TARGET_TEMPERATURE
)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the climate entity from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DaikinHttpClimate(coordinator)], True)


class DaikinHttpClimate(ClimateEntity):
    """Representation of a Daikin A/C device controlled via HTTP."""

    _attr_hvac_modes = [HVACMode.COOL, HVACMode.OFF]
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_min_temp = 16
    _attr_max_temp = 30

    def __init__(self, coordinator):
        """Initialize the climate device."""
        self.coordinator = coordinator
        self._host = coordinator.host
        self._name = (
            coordinator.config_entry.options.get("name")
            or coordinator.config_entry.data.get("name")
            or "Daikin HTTP AC"
        )
        self._attr_name = self._name
        self._hvac_mode = HVACMode.OFF
        self._target_temperature = 25
        self._current_temperature = None
        self._available = True
        self._attr_unique_id = f"daikin_http_{self._host}"

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def available(self):
        """Return True if data is available."""
        return self.coordinator.last_update_success

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self):
        """Return current HVAC mode (on/off)."""
        return self._hvac_mode

    @property
    def hvac_modes(self):
        """Return supported HVAC modes."""
        return [HVACMode.COOL, HVACMode.OFF]

    @property
    def supported_features(self):
        """Return the supported features (temperature setting)."""
        return SUPPORT_FLAGS

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._target_temperature

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._target_temperature

    #        return self.coordinator.data.get("temp")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": self._name,
            "manufacturer": "Daikin",
            "model": "HTTP API",
        }

    def _get_status(self):
        """Poll the A/C status via HTTP and update internal state."""
        try:
            resp = requests.get(f"http://{self._host}/daikinStatus?xx=1", timeout=5)
            data = resp.json()

            # 'betrieb' = 1 is ON, 0 is OFF
            self._hvac_mode = (
                HVACMode.COOL if data.get("betrieb") == 1 else HVACMode.OFF
            )
            self._target_temperature = data.get("temp", self._target_temperature)
            self._current_temperature = data.get("temp", self._current_temperature)

        except Exception as e:
            _LOGGER.error("Error getting status from Daikin unit: %s", e)
            self._available = False

    def update(self):
        """Update climate state (called by HA polling)."""
        self._get_status()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            await self.coordinator.set_temperature(temp)
            await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode (on/off)."""
        if hvac_mode == HVACMode.COOL:
            await self.coordinator.set_power(True)
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.set_power(False)
        await self.coordinator.async_request_refresh()
