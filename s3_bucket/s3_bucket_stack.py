from aws_cdk import Stack, aws_s3 as s3
from constructs import Construct
from decouple import config

# Retrieve the primary S3 bucket name from environment configuration
PRIMARY_BUCKET_NAME = config("PRIMARY_BUCKET_NAME")

# Define the S3BucketStack class that inherits from AWS CDK Stack
class S3BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the primary S3 bucket with the specified name
        s3_bucket = s3.Bucket(self, id="PrimaryBucket", bucket_name=PRIMARY_BUCKET_NAME)
