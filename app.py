#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Tags

# Define the AWS CDK environment for the stacks
env_USA = cdk.Environment(account="", region="us-west-2")

# Create an AWS CDK app
app = cdk.App()

# Instantiate stacks for different components of the system

# Create a Kinesis Stream stack
kinesis_stream = KinesisStreamStack(app, "KinesisStreamStack", env=env_USA)

# Create a Data Producer stack
data_producer = DataProducerStack(app, "DataProducerStack", env=env_USA)

# Create a Data Consumer stack
data_consumer = DataConsumerStack(app, "DataConsumerStack", env=env_USA)

# Create an S3 Bucket stack
s3_bucket = S3BucketStack(app, "S3BucketStack", env=env_USA)

# Add tags to the entire AWS CDK app
Tags.of(app).add("ProjectOwner", "Alex-Clark")
Tags.of(app).add("ProjectName", "Crypto_incremental-Pipeline")

# Synthesize the AWS CDK app to produce CloudFormation templates
app.synth()
