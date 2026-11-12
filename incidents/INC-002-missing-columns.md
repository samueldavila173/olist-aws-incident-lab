# INC-002 — Missing Required CSV Column

## 1. Incident Summary

A controlled data quality incident was simulated by removing the required `order_status` column from the header of a synthetic Olist orders CSV file.

The AWS Lambda function detected the missing column and stopped processing by raising a `ValueError`.

The incident was investigated through Amazon CloudWatch Logs and resolved by restoring the configuration to reference the valid CSV file.

## 2. System Context

The laboratory consists of:

- **Amazon S3:** Stores the CSV files.
- **AWS Lambda:** Retrieves and validates the dataset.
- **AWS IAM:** Provides permissions to access S3 and write logs.
- **Amazon CloudWatch:** Records execution events and errors.

The function is invoked manually using a Lambda test event.

## 3. Incident Reproduction

A copy of the original 20-row CSV file was created:

`olist_orders_missing_column.csv`

The `order_status` column name was removed from the CSV header.

The modified file was uploaded to the S3 bucket:

`samu-aws-incident-lab-2026`

The Lambda configuration was updated:

```python
KEY = "input/olist_orders_missing_column.csv"
```

After deploying the change, the function was invoked manually.

## 4. Incident Detection

AWS Lambda returned:

```text
Status: Failed
Error Type: ValueError
Error Message: Missing required columns: ['order_status']
```

The stack trace identified the validation failure in `lambda_function.py`, line 48.

CloudWatch recorded:

```text
Olist orders processing started
S3 GetObject successful
Olist orders processing failed
ValueError: Missing required columns: ['order_status']
```

The successful S3 retrieval confirmed that the file could be accessed.

The failure occurred during CSV schema validation.

## 5. Root Cause Analysis

The CSV header did not contain `order_status`.

As a result, the validation identified the missing field and raised an exception.

## 6. Corrective Action

The Lambda configuration was restored to reference the valid CSV file:

```python
KEY = "input/olist_orders_dataset_20_rows.csv"
```

The updated function was deployed and tested again.

## 7. Recovery Verification

The recovery test completed successfully.

| Metric | Result |
|---|---|
| Lambda execution | Succeeded |
| Application statusCode | 200 |
| Orders processed | 20 |
| Empty order IDs | 0 |
| Duplicate order IDs | 0 |
| Allocated memory | 128 MB |
| Maximum memory used | 93 MB |
| Duration | 338.76 ms |

CloudWatch confirmed:

```text
S3 GetObject successful
CSV schema validation successful
Total orders: 20
Null order IDs: 0
Duplicate order IDs: 0
Olist orders validation completed
```

## 8. Lessons Learned

1. A successful S3 retrieval does not guarantee valid input data
2. Schema validation helps prevent unexpected data structures from being processed
3. Application exceptions can identify the exact missing field
4. CloudWatch logs help distinguish data quality failures from infrastructure failures

## 9. Evidence

Screenshots documenting the failure, CloudWatch diagnosis and recovery verification will be stored in:

`evidence/incidents/INC-002/`

The evidence will be linked here once uploaded.
