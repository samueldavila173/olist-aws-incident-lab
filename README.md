# AWS Cloud Monitoring & Incident Troubleshooting Lab

## Project Overview

This project is a hands-on AWS laboratory focused on understanding application logs, investigating execution failures, and troubleshooting incidents in a cloud environment

The laboratory uses a Python-based AWS Lambda function integrated with Amazon S3 and Amazon CloudWatch to simulate data-processing operations and investigate different failure scenarios

The main objective is to follow the complete incident investigation process: observing application behavior, examining logs, identifying the root cause, applying corrective actions, and verifying the results

## Technologies Used

- **AWS Lambda:** Serverless function execution and application processing.
- **Amazon CloudWatch:** Log collection, monitoring, and error investigation.
- **Amazon S3:** Storage of input files used during testing.
- **AWS IAM:** Permission management and access troubleshooting.
- **Python:** Application logic and structured log messages.
- **JSON:** Event payloads and application responses.

## Monitoring and Troubleshooting Workflow

The laboratory follows a practical incident investigation workflow:

1. Execute the Lambda function using a test event
2. Observe the execution result and identify unexpected behavior
3. Inspect the corresponding CloudWatch log stream
4. Analyze error messages and execution details
5. Identify the probable root cause
6. Apply a corrective action to the configuration, permissions, or code
7. Run the function again to validate the correction
8. Document the incident and supporting evidence

## Incident Investigation

The repository includes documented troubleshooting scenarios involving Lambda execution, S3 interactions, and IAM permissions.

Incident reports and screenshots are available in:

- [Incident Reports](incidents/)
- [Incident Evidence](evidence/incidents/)

## Repository Structure

```text
olist-aws-incident-lab/
├── docs/                 # Technical documentation
├── evidence/
│   └── incidents/        # Screenshots and incident evidence
├── incidents/            # Incident investigation reports
├── infrastructure/       # AWS infrastructure documentation
├── src/                  # Python Lambda source code
├── .gitignore
└── README.md
```

## Key Learning Outcomes

This project provided practical experience in:

- Reading and interpreting application logs in Amazon CloudWatch.
- Investigating AWS Lambda execution errors.
- Understanding the relationship between application behavior and log messages.
- Troubleshooting S3 access and IAM permission issues.
- Validating corrective actions through repeated execution and log inspection.
- Documenting technical incidents with supporting evidence.

## Project Scope

This is a personal learning laboratory using simulated incidents in a controlled AWS environment. It is not a production deployment.

The focus is on developing practical skills in cloud monitoring, log analysis, and systematic incident troubleshooting.
