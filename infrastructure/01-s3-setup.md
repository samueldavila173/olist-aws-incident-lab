# 01 — Amazon S3 Setup

## Objective

Configure Amazon S3 as the storage layer for an AWS
data processing and incident troubleshooting laboratory

## AWS Configuration

- Service: Amazon S3
- Region: eu-north-1 (Europe - Stockholm)
- Bucket: samu-aws-incident-lab-2026
- Input prefix: input/

## Dataset

The laboratory uses the Brazilian E-Commerce
Public Dataset by Olist (Kaggle)

Initial testing uses a synthetic CSV containing
20 orders to keep resource consumption low

## Architecture

Amazon S3 → AWS Lambda → Amazon CloudWatch
for the purpose of viewing logs

## Security

AWS Lambda accesses the objects through an IAM
execution role with scoped read permissions

## Verification

The Lambda function successfully retrieved the
20 row CSV from S3 and validated its structure

## Evidence

Screenshots of the S3 configuration and successful
execution will be added to the evidence directory
