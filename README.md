# Daikin HTTP Air Conditioner Integration for Home Assistant

This is a custom integration for [Home Assistant](https://www.home-assistant.io/) that allows you to control a Daikin air conditioner over HTTP using a simple GET API.

---

## 📦 Features

- ✅ Turn Daikin A/C on and off via HTTP
- 🌡️ Set target cooling temperature
- 🔁 Periodically polls A/C status (`betrieb`, `temp`)
- 🧠 Uses `DataUpdateCoordinator` for efficient updates
- ⚙️ Configurable via UI or `configuration.yaml`

---

## 🌐 How It Works

The integration communicates with your A/C unit via the following HTTP endpoints:

| Action              | HTTP Request                                       |
|---------------------|----------------------------------------------------|
| Get status          | `http://<IP>/daikinStatus?xx=1`                    |
| Turn ON             | `http://<IP>/sendDaikin?run=1`                     |
| Turn OFF            | `http://<IP>/sendDaikin?run=0`                     |
| Set temperature     | `http://<IP>/sendDaikin?temp=<target_temp>`        |

The response to the status request must look like:

```json
{
  "betrieb": 1,
  "temp": 25,
  "ontime": 1234
}
