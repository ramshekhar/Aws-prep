import json
import boto3
import traceback

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "BlogPosts"
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    try:
        print("Received event:", json.dumps(event))  # Debugging log

        # Handle CORS preflight request (OPTIONS)
        if event.get("httpMethod") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": ""
            }

        # Fetch all posts from DynamoDB
        response = table.scan()

        # Extract posts array properly
        posts = response.get("Items", [])

        if not isinstance(posts, list):
            print("Error: Received non-array response from DynamoDB:", response)
            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Invalid data format from database"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS, GET",
                    "Access-Control-Allow-Headers": "Content-Type"
                }
            }

        print("Fetched posts:", posts)  # Debugging log

        return {
            "statusCode": 200,
            "body": json.dumps(posts),  # Ensure it's a raw JSON array
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }
    except Exception as e:
        print("Error fetching posts:", traceback.format_exc())  # Debugging log
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, GET",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }