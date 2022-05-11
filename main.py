import os
import sqlalchemy
import pandas as pd
import ast
from dotenv import load_dotenv
from datetime import datetime
import boto3


def main():
    load_dotenv()
    latest_timestamp = get_latest_timestamp()
    get_homeassistant_data(latest_timestamp)


def get_homeassistant_data(latest_timestamp):
    if os.getenv("WTW_CONNECTOR_TYPE") == "HOMEASSISTANT_RECORDER_MARIADB":
        strEngine = (
            f"mariadb+pymysql://{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_USER')}"
            f":{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_KEY')}"
            f"@{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_HOST')}:{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_PORT')}"
            f"/{os.getenv('WTW_CONNECTOR_HOMEASSISTANT_RECORDER_DATABASE')}"
        )
    else:
        exit(f"Connector type '{os.getenv('WTW_CONNECTOR_TYPE')}' not supported")

    engine = sqlalchemy.create_engine(strEngine)

    df = pd.read_sql(
        (
            "SELECT state_id,state as measure_value,attributes, created as timestamp "
            "FROM states "
            "WHERE entity_id LIKE '%%efekta%%'and state <>'unavailable' "
            f"AND created > '{latest_timestamp}' "
            "ORDER BY `states`.`created` ASC"
        ),
        engine,
    )

    dftemp = df["attributes"].apply(lambda x: ast.literal_eval(x))
    df["measure_name"] = dftemp.apply(lambda x: x.get("device_class"))
    df["unit"] = dftemp.apply(lambda x: x.get("unit_of_measurement"))
    df["friendly_name"] = dftemp.apply(lambda x: x.get("friendly_name"))
    df["friendly_name"] = df["friendly_name"].str[:5]
    df.drop("attributes", inplace=True, axis=1)
    print(df["measure_name"].unique())


def get_latest_timestamp():

    read_client = boto3.client("timestream-query")
    response = ""

    try:
        response = read_client.query(
            QueryString='SELECT Max(time) AS MaxTimestamp FROM "when-to-water"."sensor-data"'
        )
    except Exception as e:
        print(f"An exception occured: {e}")

    if response["Rows"][0]["Data"][0]["NullValue"] is True:
        return datetime.fromtimestamp(0)

    print(response)


main()
