import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("orders")

def lambda_handler(event, context):
    try:
        order_id = event["pathParameters"]["id"]

        table.delete_item(
            Key={
                "OrderId": order_id
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Order Deleted",
                "OrderId": order_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }