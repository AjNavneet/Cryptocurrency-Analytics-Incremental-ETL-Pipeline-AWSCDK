%flink.ssql

-- Create a table 'flink_test2' with specified schema using Kinesis connector
CREATE TABLE `flink_test2` (
    `from_currency_code` STRING,
    `from_currency_name` STRING,
    `to_currency_code` STRING,
    `to_currency_name` STRING,
    `exchange_rate` FLOAT,
    `last_refreshed` STRING,
    `time_zone` STRING,
    `bid_price` FLOAT,
    `ask_price` FLOAT
 )
 WITH (
   'connector' = 'kinesis',
   'stream' = 'kinesis-crypto-stream-intraday',
   'aws.region' = 'us-west-2',
   'scan.stream.initpos' = 'TRIM_HORIZON',
   'format' = 'json'
);

-- Execute a continuous query with periodic refresh
%flink.ssql(type=update, refreshInterval=1000)

-- Select distinct 'last_refreshed' and 'bid_price' from 'flink_test2'
-- where 'last_refreshed' is greater than or equal to '2023-06-06 23:00:00'
select distinct last_refreshed, bid_price from flink_test2 Where last_refreshed >= '2023-06-06 23:00:00';
