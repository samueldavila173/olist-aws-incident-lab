# AWS Lambda — Python Code Explanation

## 1. Project Objective

This AWS Lambda function processes an Olist orders CSV
file stored in Amazon S3

The main objectives are:

- Retrieve data from Amazon S3
- Validate the CSV structure
- Detect missing and duplicate order identifiers
- Generate execution logs in Amazon CloudWatch
- Return structured validation results
- Support incident investigation and troubleshooting

## 2. Python Libraries

### boto3

```python
import boto3

s3 = boto3.client("s3")
```
The boto3 library allows Python applications to
communicate with AWS services. In this project, 
it is used to retrieve CSV files from Amazon S3

The Lambda function authenticates through its
IAM execution role

### csv
```python
import csv

reader = csv.DictReader(io.StringIO(content))
```

DictReader converts each CSV row into a dictionary
using the column names as keys

This allows the function to access fields such as
order_id and customer_id

### io

```python
import io
```

The module provides tools for working with
text streams

### logging

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

The logging module records application events

These messages are available in Amazon CloudWatch
Logs and help identify processing failures

### json

```python
import json
```

It converts Python data structures
into JSON-formatted strings

## 3. AWS Resource Configuration

```python
BUCKET = "samu-aws-incident-lab-2026"
KEY = "input/olist_orders_dataset_20_rows.csv"
```

BUCKET identifies the S3 bucket

KEY identifies the object within the bucket

## 4. Lambda Handler

```python
def lambda_handler(event, context):
    request_id = context.aws_request_id
```

- lambda_handler is the entry point executed by AWS Lambda
- event: contains information about
the invocation
- context: provides execution metadata
- aws_request_id: value uniquely identifies
each Lambda invocation

## 5. Retrieving Data from Amazon S3

```python
response = s3.get_object(
    Bucket=BUCKET,
    Key=KEY
)

logger.info("S3 GetObject successful")
```

get_object: retrieves an object from S3

Potential failures include:

- AccessDenied
- NoSuchKey
- Invalid bucket configuration

These failures can be investigated using
CloudWatch logs

## 6. Reading the CSV File

```python
content = response["Body"].read().decode("utf-8-sig")

reader = csv.DictReader(io.StringIO(content))
```

- The response body contains the object data
- read: loads the object content into memory
- decode: converts the bytes into text
- UTF-8-SIG: supports UTF-8
- DictReader: interprets the CSV structure

## 7. Schema Validation

```python
columns = set(reader.fieldnames or [])

missing = REQUIRED_COLUMNS - columns

if missing:
    raise ValueError(
        f"Missing required columns: {sorted(missing)}"
    )
```

The function compares the CSV headers against
the expected columns

If any required column is missing, a ValueError
exception is raised

## 8. Data Quality Validation

### Total Orders

```python
orders = list(reader)
total_orders = len(orders)
```

The function loads the parsed rows into a list
and counts the total number of orders

### Missing Order IDs

```python
order_ids = [row["order_id"] for row in orders]

null_order_ids = sum(
    1 for order_id in order_ids
    if not order_id or not order_id.strip()
)
```

The function counts empty order identifiers

### Duplicate Order IDs

```python
duplicate_order_ids = (
    len(order_ids) - len(set(order_ids))
)
```

Subtracting the number of unique identifiers
from the total number of identifiers gives
the number of additional duplicate occurrences

If missing or duplicate IDs are detected,
the function raises a validation error

## 9. Logging and Exception Handling

```python
try:
    # Data processing operations

except Exception:
    logger.exception("Olist orders processing failed")
    raise
```

The try block contains the processing operations

If an exception occurs, logger.exception records
the error and its traceback

The raise statement propagates the exception,
allowing AWS Lambda to report a failed invocation

## 10. Successful Execution

The function successfully processed the
20 row synthetic Olist dataset

Observed results:

| Metric | Value |
|---|---|
| Execution status | Succeeded |
| Orders processed | 20 |
| Empty order IDs | 0 |
| Duplicate order IDs | 0 |
| Allocated memory | 128 MB |
| Maximum memory used | 93 MB |

## 11. Performance Limitations

The current implementation loads the complete
CSV content and parsed rows into memory

This increases memory consumption as the
dataset grows

An earlier execution using the full Olist
orders dataset failed with:

```text
Error Type: Runtime.OutOfMemory
Memory Size: 128 MB
Max Memory Used: 127 MB
```





































