import json
import boto3
import uuid
import traceback

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("orders")

REQUIRED_FIELDS = ["customerName", "product", "quantity"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        missing_fields = [
            field for field in REQUIRED_FIELDS
            if field not in body
        ]

        if missing_fields:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing required fields",
                    "missingFields": missing_fields,
                    "requiredFields": REQUIRED_FIELDS
                })
            }

        order_id = str(uuid.uuid4())

        item = {
            "OrderId": order_id,
            "customerName": body["customerName"],
            "product": body["product"],
            "quantity": body["quantity"]
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Order Created",
                "OrderId": order_id,
                "order": item
            })
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Invalid JSON body"
            })
        }

    except Exception as e:
        print("ERROR:", str(e))
        print(traceback.format_exc())

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }