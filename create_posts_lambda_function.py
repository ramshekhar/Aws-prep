import json
import boto3
import uuid
from datetime import datetime, timedelta

# Initialize the DynamoDB client
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "BlogPosts"
def get_current_time_ist():
    # Get current UTC time
    utc_now = datetime.utcnow()
    # Convert to IST (UTC +5:30)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.strftime('%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging log

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            "body": ""
        }
        
    if "body" not in event or not event["body"]:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Request body is missing"})
        }

    try:
        # Parse the request body
        body = json.loads(event["body"])
        print("Parsed body:", body)

        # Validate request
        if "title" not in body or "content" not in body:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, POST",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Title and content are required"})
            }

        # Generate unique post ID and timestamp
        post_id = str(uuid.uuid4())
        created_at =  get_current_time_ist()

        # Save post to DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                "postId": post_id,
                "title": body["title"],
                "content": body["content"],
                "createdAt": created_at
            }
        )

        print("Post successfully stored in DynamoDB")

        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Post created successfully", "postId": post_id})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }