import json
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "BlogComment"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Ensure event has httpMethod
    if "httpMethod" not in event:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Invalid request: Missing httpMethod."})
        }

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS, GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    # Handle preflight OPTIONS request
    if event["httpMethod"] == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "CORS preflight success"})}

    if event["httpMethod"] == "GET":
        if not event.get("queryStringParameters") or "postId" not in event["queryStringParameters"]:
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "postId required"})}

        post_id = event["queryStringParameters"]["postId"]

        try:
            table = dynamodb.Table(TABLE_NAME)
            response = table.scan(FilterExpression="postId = :pid", ExpressionAttributeValues={":pid": post_id})
            comments = response.get("Items", [])

            return {"statusCode": 200, "headers": headers, "body": json.dumps(comments)}

        except Exception as e:
            return {"statusCode": 500, "headers": headers, "body": json.dumps({"message": "Internal Server Error", "error": str(e)})}