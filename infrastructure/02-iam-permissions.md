# 02 — AWS IAM Permissions

## Objective

Configure secure access between AWS Lambda and Amazon S3
using IAM

## Execution Role

The Lambda function uses an IAM execution role to
access AWS services without storing credentials
directly in the Python code

Lambda function:
`samu-process-inventory`

## IAM Policies

Two policies are attached to the execution role:

### AWSLambdaBasicExecutionRole

AWS-managed policy that allows Lambda to write
execution logs to Amazon CloudWatch Logs

### SamuInventoryS3ReadOnly

Customer managed policy that grants the Lambda
function permission to read objects from the
laboratory S3 bucket

Required permission:

`s3:GetObject`

S3 resource:

`arn:aws:s3:::samu-aws-incident-lab-2026/*`

## Verification

The successful Lambda execution generated the log:

`S3 GetObject successful`

This confirms that the function was able to retrieve
the CSV object from S3 using its execution rol

## Future Incident Simulation

A controlled AccessDenied incident will be reproduced
to demonstrate how IAM permission failures can be
identified through CloudWatch logs

Status: Not yet tested
