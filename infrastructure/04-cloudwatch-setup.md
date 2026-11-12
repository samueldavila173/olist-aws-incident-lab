# 04 — Amazon CloudWatch Setup

## 1. Objective

Configure and use Amazon CloudWatch Logs to monitor
AWS Lambda executions and investigate processing failures

The laboratory focuses on cloud operations, log analysis,
data validation and incident troubleshooting

## 2. AWS Configuration

| Parameter | Value |
|---|---|
| AWS Region | eu-north-1 (Europe - Stockholm) |
| Monitoring service | Amazon CloudWatch Logs |
| Lambda function | samu-process-inventory |
| Log group | /aws/lambda/samu-process-inventory |
| Python logging level | INFO |
| Log source | AWS Lambda execution |

The Lambda execution role includes the
AWSLambdaBasicExecutionRole managed policy

This allows Lambda to write execution logs
to CloudWatch Logs

## 3. Log Generation

The Python application uses the logging module

Example:

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Olist orders processing started")
```

AWS Lambda also generates platform logs, including:

- START: Beginning of an invocation
- END: End of an invocation
- REPORT: Execution duration and memory metrics

## 4. Successful Execution Analysis

The synthetic Olist dataset contains 20 orders.

The following messages were observed:

```text
Olist orders processing started
S3 GetObject successful
CSV schema validation successful
Total orders: 20
Null order IDs: 0
Duplicate order IDs: 0
Olist orders validation completed
```

Execution metrics:

| Metric | Result |
|---|---|
| Status | Succeeded |
| Duration | 206.76 ms |
| Allocated memory | 128 MB |
| Maximum memory used | 93 MB |
| Orders processed | 20 |
| Null order IDs | 0 |
| Duplicate order IDs | 0 |

These results confirm successful processing
of the dataset

## 5. RequestId and Traceability

The RequestId helps correlate log messages belonging
to the same execution

This is useful when investigating multiple executions
within the same CloudWatch log group

## 6. Error Investigation

When a failure occurs, the investigation follows
this workflow:

1. Identify the failed invocation
2. Locate its RequestId
3. Review application and platform logs
4. Identify the error type and stack trace
5. Determine the likely root cause
6. Apply a corrective action
7. Run a new test
8. Verify recovery and document the evidence

## 7. Known Incident: OutOfMemory

An execution using the full Olist orders dataset
failed with:

```text
Error Type: Runtime.OutOfMemory
Memory Size: 128 MB
Max Memory Used: 127 MB
```

## 8. Current Limitations

- Logs are reviewed manually
- CloudWatch alarms have not been configured
- No automatic incident ticket creation exists
- Grafana and Loki are not connected
- No centralized monitoring dashboard has been built

