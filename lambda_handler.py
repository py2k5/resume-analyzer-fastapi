import json
import base64
from mangum import Mangum
from main import app

# Create the Lambda handler
handler = Mangum(app)

# Alternative simple handler for testing
def lambda_handler(event, context):
    """
    AWS Lambda handler for the Resume Analyzer API
    """
    try:
        # Use Mangum to handle the ASGI app
        return handler(event, context)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }
