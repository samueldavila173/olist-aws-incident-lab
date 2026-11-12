import boto3
import csv
import io
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

BUCKET = "samu-aws-incident-lab-2026"
KEY = "input/olist_orders_dataset_20_rows.csv"

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
}


def lambda_handler(event, context):
    request_id = context.aws_request_id

    logger.info("Olist orders processing started")
    logger.info("RequestId: %s", request_id)

    try:
        response = s3.get_object(
            Bucket=BUCKET,
            Key=KEY
        )

        logger.info("S3 GetObject successful")

        content = response["Body"].read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))

        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        orders = list(reader)
        total_orders = len(orders)

        logger.info("CSV schema validation successful")
        logger.info("Total orders: %s", total_orders)

        order_ids = [row["order_id"] for row in orders]

        null_order_ids = sum(
            1 for order_id in order_ids
            if not order_id or not order_id.strip()
        )

        duplicate_order_ids = (
            len(order_ids) - len(set(order_ids))
        )

        logger.info("Null order IDs: %s", null_order_ids)
        logger.info("Duplicate order IDs: %s", duplicate_order_ids)

        if null_order_ids > 0 or duplicate_order_ids > 0:
            raise ValueError(
                "Data quality validation failed"
            )

        logger.info("Olist orders validation completed")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "total_orders": total_orders,
                "null_order_ids": null_order_ids,
                "duplicate_order_ids": duplicate_order_ids,
                "request_id": request_id
            })
        }

    except Exception:
        logger.exception("Olist orders processing failed")
        raise
