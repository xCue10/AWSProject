import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'PantryItems') # Default to 'PantryItems'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    # Handle CORS preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE' # Ensure all methods are allowed for CORS
            },
            'body': ''
        }

    item_id = None
    # Check if itemID is present in path parameters (for fetching a single item)
    if 'pathParameters' in event and event['pathParameters'] and 'itemID' in event['pathParameters']:
        item_id = event['pathParameters']['itemID']
        print(f"Attempting to fetch single item with ID: {item_id}")

    try:
        if item_id:
            # Fetch a single item by itemID
            response = table.get_item(
                Key={
                    'itemID': item_id # Note: 'itemID' (capital D) to match your DynamoDB primary key
                }
            )
            item = response.get('Item')
            
            if item:
                print(f"Successfully fetched single item: {json.dumps(item)}")
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps(item) # Return the single item directly
                }
            else:
                print(f"Item with ID {item_id} not found.")
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({'message': f'Item with ID {item_id} not found.'})
                }
        else:
            # Fetch all items (existing functionality)
            response = table.scan() # scan is generally used for small tables for all items
            items = response.get('Items', [])
            
            # Sort items by dateAdded in descending order (most recent first)
            items.sort(key=lambda x: x.get('dateAdded', ''), reverse=True)

            # Convert Decimal types to float/int if present, for JSON serialization
            # (DynamoDB's DocumentClient handles this automatically in Node.js/Python,
            # but if you use standard boto3 client and scan/get, it might return Decimal.
            # It's good practice to ensure JSON serializability for all data.)
            for item in items:
                for key, value in item.items():
                    if isinstance(value, type(boto3.dynamodb.types.Decimal('1'))): # Check for Decimal type
                        item[key] = int(value) if value % 1 == 0 else float(value)


            print(f"Successfully fetched {len(items)} items.")
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'items': items}) # Return list of items wrapped in 'items' key
            }

    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Failed to fetch items', 'error': str(e)})
        }