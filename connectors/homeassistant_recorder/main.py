import os
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

if os.getenv("WTW_CONNECTOR_TYPE") == "HOMEASSISTANT_RECORDER_MARIADB":
    strEngine = (
        f"mariadb+mariadbconnector://{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_USER')}"
        f":{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_KEY')}"
        f"@{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_HOST')}:{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_PORT')}"
        f"/{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_DATABASE')}"
    )
else:
    exit(f"Connector type '{os.getenv('WTW_CONNECTOR_TYPE')}' not supported")

engine = sqlalchemy.create_engine(strEngine)

df = pd.read_sql(
    (
        "SELECT state_id,entity_id,state,attributes, "
        "last_changed,last_updated,created,old_state_id "
        "FROM states "
        "WHERE entity_id LIKE '%efekta%'and state <>'unavailable' "
        "ORDER BY `states`.`created` DESC"
    ),
    engine,
)

# Results
print(df.head(5))
