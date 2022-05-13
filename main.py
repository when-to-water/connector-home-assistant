import argparse
import ast
import os
from datetime import datetime

import boto3
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv


def main():
    load_dotenv()

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--dump-hass-df",
        nargs="?",
        default=False,
        const=True,
        help="dump homeassistant dataframe to json file (./hass.json)",
    )
    args = argparser.parse_args()

    if args.dump_hass_df is False:
        latest_timestamp = get_latest_timestamp()
        df = get_homeassistant_data(latest_timestamp)
        sent_data_to_timestream(df)
    else:
        print("Dumping homeassistant dataframe to json file (./hass.json)")
        df = get_homeassistant_data(datetime.fromtimestamp(0))
        df.to_json("./hass.json")


def get_homeassistant_data(latest_timestamp):

    if os.path.exists("./hass.json"):
        df = pd.read_json("./hass.json")
        return df

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

    try:
        df = pd.read_sql(
            (
                "SELECT state as MeasureValue,attributes, UNIX_Timestamp(CONVERT_TZ(created,'+02:00','+00:00')) as Time "
                "FROM states "
                "WHERE entity_id LIKE '%%efekta%%'and state <>'unavailable' "
                "AND created > %(latest_timestamp)s "
                "ORDER BY `states`.`created` DESC"
            ),
            engine,
            params={"latest_timestamp": latest_timestamp},
        )
    except Exception as e:
        print(f"An exception occured: {e}")

    dftemp = df["attributes"].apply(lambda x: ast.literal_eval(x))
    df["Unit"] = dftemp.apply(lambda x: x.get("unit_of_measurement"))
    df["SensorName"] = dftemp.apply(lambda x: x.get("friendly_name"))
    df["MeasureName"] = df["SensorName"].str.split(" ").str[1]
    df["SensorName"] = df["SensorName"].str[:5]
    df["Time"] = df["Time"].round(0).astype(int).apply(str)
    df = df[df["SensorName"].isin(["PWS_1", "PWS_2", "PWS_3"])]
    df.drop("attributes", inplace=True, axis=1)
    print(df.head())
    return df


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


def sent_data_to_timestream(df):

    write_client = boto3.client("timestream-write")
    DB_NAME = "when-to-water"
    TBL_NAME = "sensor-data"
    response = ""

    for x in pd.unique(df["SensorName"]):
        for y in pd.unique(df["Unit"]):
            records = []
            common_attributes = {
                "Dimensions": [
                    {"Name": "SensorName", "Value": x},
                    {"Name": "Unit", "Value": y},
                ],
                "MeasureValueType": "DOUBLE",
                "TimeUnit": "SECONDS",
            }
            dftemp = df[(df["SensorName"] == x) & (df["Unit"] == y)]
            dftemp = dftemp.drop(columns=["SensorName", "Unit"])
            records = dftemp.to_dict(orient="records")
            print(common_attributes)
            try:
                response = write_client.write_records(
                    DatabaseName=DB_NAME,
                    TableName=TBL_NAME,
                    Records=records,
                    CommonAttributes=common_attributes,
                )
                print(
                    f"WriteRecords Status: [{response['ResponseMetadata']['HTTPStatusCode']}]"
                )
            except write_client.exceptions.RejectedRecordsException as e:
                print("RejectedRecords: ", e)
                for rr in e.response["RejectedRecords"]:
                    print(f"Rejected Index {str(rr['RecordIndex'])}: {rr['Reason']}")
            except Exception as e:
                print(f"An exception occured: {e}")


main()
