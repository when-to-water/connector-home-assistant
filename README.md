# Home Assistant Connector

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

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

### Installation

```Shell
pipenv install
```

### Run

```Shell
pipenv shell
python main.py
```

## Docker

Fill the aws `credentials`-file in /aws/credentials:
```
[default]
region=<AWS_REGION>
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```

### Build
Navigate to the directory of the Dockerfile and run:
```Shell
docker build -t connector-hass .
```

### Run container
```Shell
docker run -dt -v $(pwd):/home/awsuser/connector-hass --name connector-hass onnector-hass
```