# 03 — AWS Lambda Setup

## 1. Objective

Configure an AWS Lambda function to process and validate
CSV files stored in Amazon S3

The lab uses a synthetic 20-row sample from a real-world dataset

The objective is to practice cloud data processing,
logging, data quality validation and troubleshooting

## 2. Lambda Configuration

| Parameter | Configuration |
|---|---|
| AWS Region | eu-north-1 (Europe - Stockholm) |
| Function name | samu-process-inventory |
| Runtime | Python 3.13 |
| Memory | 128 MB |
| Execution role | Dedicated IAM execution role |
| Trigger | Manual invocation using a test event |
| Source | Amazon S3 |

The function is currently invoked manually

## 3. Data Source

S3 bucket:

`samu-aws-incident-lab-2026`

Object key:

`input/olist_orders_dataset_20_rows.csv`

The original Olist dataset is considerably larger
and was used in an earlier memory-failure test

## 4. Processing Workflow

1. Lambda starts execution
2. The function connects to Amazon S3 using boto3
3. It retrieves the CSV object
4. Python parses the CSV file
5. The required columns are validated
6. The total number of orders is calculated
7. Empty order IDs are counted
8. Duplicate order IDs are counted
9. Validation results are written to CloudWatch
10. The function returns a JSON response

## 5. Data Quality Checks

The function checks the presence of these columns:

- order_id
- customer_id
- order_status
- order_purchase_timestamp
- order_approved_at
- order_delivered_carrier_date
- order_delivered_customer_date
- order_estimated_delivery_date

## 6. Logging

Python's logging module is used to generate
execution messages

Logs are collected in Amazon CloudWatch Logs.

Log group:

`/aws/lambda/samu-process-inventory`

## 7. Successful Execution

The function was tested using the AWS Lambda console.

Test event name:

`cloudwatch-logs`

Observed result:

| Metric | Value |
|---|---|
| Execution status | Succeeded |
| HTTP-style statusCode | 200 |
| Orders processed | 20 |
| Empty order IDs | 0 |
| Duplicate order IDs | 0 |
| Allocated memory | 128 MB |
| Maximum memory used | 93 MB |

The function successfully read and validated
the synthetic CSV sample

## 8. Known Limitations

The current implementation loads the complete CSV
into memory

This approach is suitable for small files but
can lead to excessive memory consumption with
larger datasets

A previous execution using the full Olist orders
dataset failed with Runtime.OutOfMemory

## 9. Next Improvements

- Implement streaming CSV processing
- Add structured logging
- Validate additional data quality rules
- Introduce automated S3 event triggers
- Add unit tests
- Document controlled failure scenarios
