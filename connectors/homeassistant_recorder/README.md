# Home Assistant Connector

Reads data from the [recorder integration](https://www.home-assistant.io/integrations/recorder/) of [Home Assistant](https://www.home-assistant.io/). Currently only the _RECORDER_-Backend is supported.
Set environment variables with connection data and conenctor setting or use `.env`-file:
```
WTW_CONNECTOR_TYPE=HOMEASSISTANT_RECORDER_MARIADB
WTW_CONNECTOR_HOMEASSISTANT_RECORDER_USER=
WTW_CONNECTOR_HOMEASSISTANT_RECORDER_KEY=
WTW_CONNECTOR_HOMEASSISTANT_RECORDER_HOST=
WTW_CONNECTOR_HOMEASSISTANT_RECORDER_PORT=
WTW_CONNECTOR_HOMEASSISTANT_RECORDER_DATABASE=
```

## Installation

```Shell
pipenv install
```

## Run

```Shell
pipenv shell
python main.py
```
