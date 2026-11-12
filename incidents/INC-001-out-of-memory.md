# INC-001 — AWS Lambda OutOfMemory

## 1. Incident Summary

During the development of an AWS-based data processing laboratory, an AWS Lambda function failed while processing the full Olist Brazilian E-Commerce orders dataset

The function was configured with 128 MB of memory and used Python to retrieve, parse and validate a CSV file stored in Amazon S3

The execution failed with the following error:

```text
Runtime.OutOfMemory
```

The incident highlighted a scalability limitation in the initial CSV processing implementation

## 2. System Context

The laboratory architecture consisted of:

- **Amazon S3:** Storage for the Olist CSV dataset
- **AWS Lambda:** Python-based CSV processing and validation
- **AWS IAM:** Permissions allowing Lambda to retrieve objects from S3
- **Amazon CloudWatch:** Execution logs and diagnostic information

## 3. Incident Detection

The failure was detected during a manual Lambda test

The function started successfully and retrieved the CSV object from S3

CloudWatch recorded:

```text
Olist orders processing started
S3 GetObject successful
```

However, the execution did not complete the data validation process

The Lambda execution report contained:

```text
RequestId: ea080b7a-bb48-490b-b386-61af7c572cc9

Duration: 2181.27 ms
Billed Duration: 2672 ms

Memory Size: 128 MB
Max Memory Used: 127 MB

Status: error
Error Type: Runtime.OutOfMemory
```

These logs confirmed that the Lambda runtime exhausted its available memory

## 4. Root Cause Analysis

The original Python implementation loaded the entire CSV file into memory:

```python
content = response["Body"].read().decode("utf-8-sig")

reader = csv.DictReader(io.StringIO(content))

orders = list(reader)
```

This approach was sufficient for small CSV files but became unsuitable for the larger Olist dataset under the configured 128 MB memory limit

**Root cause:** Excessive memory consumption during CSV processing relative to the allocated Lambda memory

## 5. Corrective Action

To continue developing and testing the laboratory without increasing allocated resources, the full dataset was replaced with a smaller CSV containing 20 orders

```python
KEY = "input/olist_orders_dataset_20_rows.csv"
```

This action reduced the test workload

## 6. Recovery Verification

After changing the input file, the Lambda function was executed again

The test completed successfully

| Metric                 | Result    |
| ---------------------- | --------- |
| Execution status       | Succeeded |
| Application statusCode | 200       |
| Orders processed       | 20        |
| Empty order IDs        | 0         |
| Duplicate order IDs    | 0         |
| Allocated memory       | 128 MB    |
| Maximum memory used    | 93 MB     |
| Execution duration     | 206.76 ms |

The logs confirmed that the function could retrieve and validate the smaller dataset

## 7. Lessons Learned

This incident demonstrated several important operational concepts:

1. Successful S3 access does not guarantee successful downstream processing
2. Lambda memory limits must be considered when processing large datasets
3. CloudWatch execution reports provide useful diagnostic metrics
4. Application logs help identify the last successfully completed processing stage

## 8. Preventive and Future Actions

The following improvements are planned:

- Replace full-file loading with streaming CSV processing
- Avoid unnecessary in-memory copies of parsed records

## 9. Incident Status

**Current status:** Mitigated for the 20-row laboratory dataset

## 10. Evidence

The incident was confirmed through AWS Lambda and Amazon CloudWatch execution logs.

Supporting screenshots will be stored under:

`evidence/incidents/INC-001/`

Evidence should include:

- Failed Lambda execution
- CloudWatch `Runtime.OutOfMemory` report
- Successful execution using the 20-row dataset
