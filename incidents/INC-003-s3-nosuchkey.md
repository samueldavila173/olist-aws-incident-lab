# INC-003 — Amazon S3 NoSuchKey

## 1. Incident Summary

A controlled incident was simulated by configuring AWS Lambda to retrieve a nonexistent CSV object from Amazon S3.

The first execution returned `AccessDenied` because the Lambda execution role did not have permission to perform `s3:ListBucket`.

After temporarily granting restricted `s3:ListBucket` permission, the same missing object produced `NoSuchKey`.

The Lambda function was then restored to use the valid Olist CSV dataset, and successful processing was verified.

## 2. System Context

The laboratory uses:

- Amazon S3 for CSV storage.
- AWS Lambda for Python-based data validation.
- AWS IAM for access control.
- Amazon CloudWatch for log analysis.

## 3. Incident Reproduction

The Lambda configuration was changed to:

```python
KEY = "input/olist_orders_not_found.csv"
```

This object did not exist in the laboratory bucket.

The function attempted to retrieve it using:

```python
response = s3.get_object(
    Bucket=BUCKET,
    Key=KEY
)
```

## 4. Initial Failure — AccessDenied

The first test returned:

```text
AccessDenied

No identity-based policy allows
the s3:ListBucket action.
```

The execution role had permission to read objects but lacked permission to list the bucket.

For a nonexistent object, S3 can return `AccessDenied` when the requester lacks `s3:ListBucket`.

## 5. IAM Investigation

A temporary inline policy named `TemporaryListBucketINC003` was added to the Lambda execution role.

It granted `s3:ListBucket` on the laboratory bucket, restricted by an `s3:prefix` condition.

After the permission became effective, the test was repeated.

## 6. Confirmed Failure — NoSuchKey

The second test returned:

```text
Error Type: NoSuchKey

An error occurred (NoSuchKey) when calling
the GetObject operation:
The specified key does not exist.
```

This confirmed that the configured object key did not exist.

CloudWatch recorded the exception and its traceback.

## 7. Corrective Action

The Lambda configuration was restored:

```python
KEY = "input/olist_orders_dataset_20_rows.csv"
```

The temporary IAM permission was designated for removal after the investigation.

The original S3 read permissions were retained.

## 8. Recovery Verification

The Lambda function successfully processed the valid CSV.

| Metric | Result |
|---|---|
| Execution | Succeeded |
| statusCode | 200 |
| Orders processed | 20 |
| Null order IDs | 0 |
| Duplicate order IDs | 0 |
| Allocated memory | 128 MB |
| Maximum memory used | 93 MB |
| Duration | 360.56 ms |

CloudWatch recorded:

```text
S3 GetObject successful
CSV schema validation successful
Total orders: 20
Null order IDs: 0
Duplicate order IDs: 0
Olist orders validation completed
```

## 9. Lessons Learned

1. `AccessDenied` does not always mean that an existing object cannot be read.
2. S3 object-existence responses can depend on IAM permissions.
3. CloudWatch helps identify the operation that failed.
4. Temporary diagnostic permissions should be narrowly scoped and removed after testing.

## 10. Evidence

Evidence will be stored under:

`evidence/incidents/INC-003/`

The evidence will document:

- Initial `AccessDenied` response.
- Confirmed `NoSuchKey` response.
- CloudWatch logs.
- Successful Lambda recovery.

## 11. Final Status

Application processing has been restored and verified.

The incident can be marked fully closed after confirming removal of the temporary IAM policy.
