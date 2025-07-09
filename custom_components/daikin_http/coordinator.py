import logging
import asyncio
import aiohttp
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
import json


_LOGGER = logging.getLogger(__name__)


class DaikinCoordinator(DataUpdateCoordinator):
    """Coordinator to poll Daikin HTTP API."""

    def __init__(self, hass: HomeAssistant, host: str, config_entry):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Daikin HTTP Coordinator",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.config_entry = config_entry
        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        """Fetch data from the A/C."""
        url = f"http://{self.host}/daikinStatus?xx=1"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    text = await resp.text()
                    data = json.loads(text)
                    return {"betrieb": data.get("betrieb"), "temp": data.get("temp")}
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

    async def set_power(self, turn_on: bool):
        """Send power command to A/C."""
        url = f"http://{self.host}/sendDaikin?run={'1' if turn_on else '0'}"
        _LOGGER.debug("Setting run mode to %s, %s", turn_on, url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                text = await resp.text()
                _LOGGER.debug("response %s", text)

    async def set_temperature(self, temperature: float):
        """Set target temperature."""
        url = f"http://{self.host}/sendDaikin?temp={int(temperature)}"
        _LOGGER.debug("Setting temperature to %s, %s", temperature, url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                text = await resp.text()
                _LOGGER.debug("response %s", text)
