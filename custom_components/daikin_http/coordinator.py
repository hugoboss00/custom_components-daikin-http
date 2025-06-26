import logging
import aiohttp
import json
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


class DaikinCoordinator(DataUpdateCoordinator):
    """Coordinator to poll Daikin HTTP API."""

    def __init__(self, hass, host: str):
        """Initialize."""
        self.host = host
        super().__init__(
            hass,
            _LOGGER,
            name="Daikin HTTP Coordinator",
            update_interval=timedelta(seconds=30),
        )

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
