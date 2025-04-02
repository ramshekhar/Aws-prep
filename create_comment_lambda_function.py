import json
import boto3
import uuid
from datetime import datetime, timedelta

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "BlogComment"
def get_current_time_ist():
    # Get current UTC time
    utc_now = datetime.utcnow()
    # Convert to IST (UTC +5:30)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.strftime('%Y-%m-%d %H:%M:%S')

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
        "Access-Control-Allow-Methods": "OPTIONS, POST",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    # Handle preflight OPTIONS request
    if event["httpMethod"] == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "CORS preflight success"})}

    if event["httpMethod"] == "POST":
        try:
            body = json.loads(event["body"]) if "body" in event and event["body"] else {}

            if "postId" not in body or "comment" not in body:
                return {"statusCode": 400, "headers": headers, "body": json.dumps({"message": "postId and comment required"})}

            comment_id = str(uuid.uuid4())
            created_at =  get_current_time_ist()

            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item={"commentId": comment_id, "postId": body["postId"], "comment": body["comment"], "createdAt": created_at})

            return {"statusCode": 201, "headers": headers, "body": json.dumps({"message": "Comment created", "commentId": comment_id})}

        except Exception as e:
            return {"statusCode": 500, "headers": headers, "body": json.dumps({"message": "Internal Server Error", "error": str(e)})}
