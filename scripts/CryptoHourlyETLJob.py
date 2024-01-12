import sys
import boto3
from boto3.dynamodb.conditions import Key, Attr
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from datetime import datetime, timedelta

# Get the job name from command-line arguments
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

# Initialize Spark context, Glue context, Spark session, and Glue job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Set Spark configuration for dynamic partition overwrite
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

# Define constants for time range, start date, end date, and data location
HOURS = 2
START_DATE = (datetime.now() - timedelta(hours=HOURS)).strftime("%Y-%m-%d %H:00:00")
END_DATE = datetime.now().strftime("%Y-%m-%d %H:00:00")
LOCATION = "s3://crypto-incremental-project/data/intraday_data/"

# Function to retrieve data from DynamoDB within a specified time range
def get_dynamodb_data(start_date, end_date):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("crypto_intraday")
    filter_expression = Key("last_refreshed").between(start_date, end_date)
    response = table.scan(FilterExpression=filter_expression)
    return response["Items"]

# Function to create a DataFrame from DynamoDB items
def create_df_from_items(items: list):
    rdd = sc.parallelize(items)
    df = rdd.toDF()
    return df

# Function to convert string timestamp to Spark timestamp
def string_to_timestamp(df, col_name: str):
    return df.withColumn(col_name, F.to_timestamp(col_name))

# Function to add Simple Moving Averages (SMA) columns to the DataFrame
def add_sma(df, column: str, period: int, partition_col: str, sort_col: str):
    col_name = f"sma_{period}"
    return df.withColumn(
        col_name,
        F.avg(column).over(
            Window.partitionBy(F.col(partition_col))
            .orderBy(F.col(sort_col))
            .rowsBetween(-period, 0)
        ),
    )

# Function to add SMA columns for multiple periods
def add_sma_cols(df):
    for period in [10, 30, 60, 100]:
        df = add_sma(df, "bid_price", period, "ticker", "last_refreshed")
    return df

# Function to add partition columns for date and hour
def add_partition_cols(df):
    return df.withColumn("date", F.to_date("last_refreshed")).withColumn(
        "hour", F.format_string("%02d", F.hour("last_refreshed"))
    )

# Function to write DataFrame to specified location
def write_df(df):
    df.write.partitionBy("ticker", "date", "hour").mode("overwrite").format(
        "parquet"
    ).save(LOCATION)

# Get data from DynamoDB, create DataFrame, and perform required transformations
items = get_dynamodb_data(START_DATE, END_DATE)
df = create_df_from_items(items)
df = string_to_timestamp(df, "last_refreshed")
df = add_sma_cols(df)
df = add_partition_cols(df)

# Write the DataFrame to the specified location in Parquet format
write_df(df)

# Commit the Glue job
job.commit()
