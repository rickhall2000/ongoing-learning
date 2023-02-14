import json

# This function will accept an audio file and return a transcription
# params are multipart form containing wavfile and language


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                   },
}

