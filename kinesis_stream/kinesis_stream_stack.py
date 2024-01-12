from aws_cdk import Stack, aws_kinesis as kinesis, Duration
from constructs import Construct
from decouple import config

# Retrieve the Intraday Kinesis Stream name from environment configuration
INTRADAY_STREAM_NAME = config("INTRADAY_STREAM_NAME")

# Define the KinesisStreamStack class that inherits from AWS CDK Stack
class KinesisStreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Intraday Kinesis Stream with specified settings
        intraday_stream = kinesis.Stream(
            self,
            "IntradayKinesisStream",
            stream_name=INTRADAY_STREAM_NAME,
            shard_count=1,
            retention_period=Duration.hours(24),
        )
