import json
from cgi import parse_header, parse_multipart
from io import BytesIO
# from streaming_form_data import StreamingFormDataParser
# from streaming_form_data.targets import ValueTarget
import base64
import boto3

# This function will accept an audio file and return a transcription
# params are multipart form containing wavfile and language


def lambda_handler(event, context):
    print("Transcribe called")

    x = event.get("body", {})

    c_type, c_data = parse_header(event['headers']['Content-Type'])
    print("line 1")
    assert c_type == 'multipart/form-data'
    print("line 2")
#    form_data = parse_multipart(BytesIO(event['body'].decode('base64')), c_data)
#    form_data = parse_multipart(c_data, {})
    print("line 3")
#    print(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                   },
}

