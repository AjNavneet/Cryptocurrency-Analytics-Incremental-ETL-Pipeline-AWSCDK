# Cryptocurrency Analytics using Incremental ETL Pipeline with AWS CDK

## Business Overview

Cryptocurrency refers to digital or virtual currencies that use cryptography for secure financial transactions, control the creation of additional units, and verify the transfer of assets. Cryptocurrencies leverage decentralized technology called blockchain, which is a distributed ledger maintained by a network of computers.

The most well-known and widely used cryptocurrency is Bitcoin, which was introduced in 2009. Bitcoin was the first decentralized cryptocurrency and remains the largest by market capitalization. Since the creation of Bitcoin, thousands of other cryptocurrencies, often referred to as altcoins (alternative coins), have been developed.

Cryptocurrency data analytics plays a crucial role in understanding trends, making informed decisions, and identifying opportunities within the crypto space. Key aspects include:

- **Market Data Analysis:** Analyzing historical and real-time market data.
- **Blockchain Analysis:** Understanding transaction flows, addresses, and network behavior.
- **Sentiment Analysis:** Gauging sentiment and public perception.
- **Trading Strategies and Predictive Modeling:** Applying machine learning to develop trading strategies.
- **Risk Assessment and Security:** Assessing risks associated with cryptocurrencies.

Cryptocurrency data analytics can be performed using various tools and platforms, including charting platforms, data visualization tools, sentiment analysis tools, and machine learning libraries.

---

## Objective

We aim to develop an incremental Extract, Transform, Load (ETL) solution utilizing AWS CDK to analyze cryptocurrency data. The solution involves:

- Constructing a serverless pipeline using Lambda functions to retrieve data from an API and stream it into Kinesis streams.
- Creating a Lambda function to consume the data from the Kinesis stream, apply necessary transformations, and store it in DynamoDB.

Data analytics on the incoming data within the Kinesis streams will be performed using Apache Flink and Apache Zeppelin. AWS serverless technologies, such as Amazon Lambda and Amazon Glue, will be employed to efficiently process and transform the data from three different sources.

We will utilize Amazon Athena, a query service, to analyze the transformed data stored in DynamoDB, facilitating efficient querying and exploration of the data.

---

## Dataset Description

Alpha Vantage offers enterprise-grade financial market data via a collection of robust and developer-friendly data APIs and spreadsheets, including real-time and historical global market data.

---

## Tech Stack

- **Language:** `Python`
- **Services:** `AWS S3`, `Amazon Lambda`, `Amazon Aurora`, `AWS Glue`, `Amazon Athena`, `Quicksight`, `AWS CDK`

---

## AWS CDK

The AWS Cloud Development Kit (AWS CDK) is an open-source software development platform for defining cloud architecture in code and provisioning it using AWS CloudFormation. It provides a high-level object-oriented framework for defining AWS resources with the capability of current programming languages.

---

## Setup

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

Create a file called .env with the environment variables needed, make sure to can your own API Key from Alpha Vantage.

```
$ touch .env
$ echo 'INTRADAY_STREAM_NAME=kinesis-crypto-stream-intraday' >> .env
$ echo 'API_KEY=[YOUR_API_KEY]' >> .env
$ echo 'LAMBDA_PRODUCER_NAME=crypto_data_producer' >> .env
$ echo 'LAMBDA_CONSUMER_NAME=crypto_data_consumer' >> .env
$ echo 'DYNAMO_TABLE_NAME=crypto_intraday' >> .env
$ echo 'PRIMARY_BUCKET_NAME=crypto-incremental-project' >> .env
```

In order to install the Alpha Vantage Layer, do the following:

```
$ mkdir -p layers/alpha_vantage_layer/python
$ pip install -t layers/alpha_vantage_layer/python/ urllib3==1.26.16 alpha_vantage
```
