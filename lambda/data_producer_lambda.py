import os
from alpha_vantage.foreignexchange import ForeignExchange
from datetime import datetime
import json
import boto3
import time
import math

# Retrieve environment variables
API_KEY = os.environ["API_KEY"]
INTRADAY_STREAM_NAME = os.environ["INTRADAY_STREAM_NAME"]
BATCH_LIMIT = 500

# Define keys for renaming and conversion
DICT_KEYS = [
    ("1. From_Currency Code", "from_currency_code"),
    ("2. From_Currency Name", "from_currency_name"),
    ("3. To_Currency Code", "to_currency_code"),
    ("4. To_Currency Name", "to_currency_name"),
    ("5. Exchange Rate", "exchange_rate"),
    ("6. Last Refreshed", "last_refreshed"),
    ("7. Time Zone", "time_zone"),
    ("8. Bid Price", "bid_price"),
    ("9. Ask Price", "ask_price"),
]

FLOAT_KEYS = ["exchange_rate", "bid_price", "ask_price"]

# Utility function to rename dictionary key
def rename_dict_key(dct: dict, old_name: str, new_name: str) -> None:
    dct[new_name] = dct.pop(old_name)

# Utility function to rename multiple dictionary keys
def rename_dict_keys(dct: dict, keys: list):
    for key in keys:
        rename_dict_key(dct, key[0], key[1])

# Utility function to convert specified keys in a dictionary to floats
def convert_floats(dct: dict, keys: list) -> None:
    for key in keys:
        try:
            dct[key] = float(dct[key])
        except Exception as e:
            raise

# Cleanup function to standardize dictionary keys and convert specified values to floats
def cleanup_data(dct: dict) -> None:
    rename_dict_keys(dct, DICT_KEYS)
    convert_floats(dct, FLOAT_KEYS)

# Function to fetch cryptocurrency data using Alpha Vantage API
def get_crypto_data(from_currency, to_currency):
    cc = ForeignExchange(API_KEY)
    data, _ = cc.get_currency_exchange_rate(
        from_currency=from_currency, to_currency=to_currency
    )
    cleanup_data(data)
    return data

# Function to create a partition key from the last_refreshed timestamp
def create_partition_from_date(last_refreshed: str) -> str:
    dt = datetime.strptime(last_refreshed, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%dT%H:00:00Z")

# Function to handle intraday request, send data to Kinesis stream
def handle_intraday_request(from_currency, to_currency):
    client = boto3.client("kinesis")
    data = get_crypto_data(from_currency, to_currency)
    partition_key = create_partition_from_date(data["last_refreshed"])
    response = client.put_record(
        StreamName=INTRADAY_STREAM_NAME,
        Data=json.dumps(data).encode("utf-8"),
        PartitionKey=partition_key,
    )
    return response

# Lambda function handler
def handler(event, context):
    assert "from_currency" in event.keys(), "Event must include key 'from_currency'"
    assert "to_currency" in event.keys(), "Event must include key 'to_currency'"
    from_currency = event["from_currency"]
    to_currency = event["to_currency"]
    response = handle_intraday_request(from_currency, to_currency)
    return response
