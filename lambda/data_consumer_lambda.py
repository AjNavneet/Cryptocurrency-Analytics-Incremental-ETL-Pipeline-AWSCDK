import os
import boto3
import json
import base64
from decimal import Decimal

# Retrieve the DynamoDB table name from environment variables
TABLE_NAME = os.environ["DYNAMO_TABLE_NAME"]

# Define the Lambda function handler
def handler(event, context):
    # Initialize DynamoDB resource and connect to the specified table
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)

    # Process each record from the Kinesis stream
    for record in event["Records"]:
        # Decode and parse the base64-encoded Kinesis record payload
        payload = base64.b64decode(record["kinesis"]["data"])
        data = json.loads(payload.decode("utf-8"), parse_float=Decimal)

        # Enhance the data by creating a "ticker" field based on currency codes
        data["ticker"] = data["from_currency_code"] + data["to_currency_code"]

        # Insert the processed data into the DynamoDB table
        table.put_item(Item=data)
