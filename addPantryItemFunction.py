import json
import boto3
import uuid
import os
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'PantryItems')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    try:
        if 'body' in event:
            try:
                request_body = json.loads(event['body'])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON body: {e}")
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        else:
            request_body = event 

        item_name = request_body.get('itemName')
        quantity = request_body.get('quantity', 1)
        # --- NEW: Get category and containerType ---
        category = request_body.get('category', 'Other') # Default to 'Other' if not provided
        container_type = request_body.get('containerType', 'N/A') # Default to 'N/A'

        if not item_name:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': "Missing 'itemName' in request body"})
            }

        item_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        item_to_save = {
            'itemID': item_id,
            'itemName': item_name,
            'quantity': int(quantity),
            'dateAdded': timestamp,
            # --- NEW: Add category and containerType to the item ---
            'category': category,
            'containerType': container_type
        }
        
        print(f"Attempting to save item: {json.dumps(item_to_save)}")
        table.put_item(Item=item_to_save)
        print("Item saved successfully.")

        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Pantry item added successfully!',
                'itemID': item_id,
                'item': item_to_save 
            })
        }

    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Could not process request', 'details': str(e)})
        }