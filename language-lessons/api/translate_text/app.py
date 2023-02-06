import json
import boto3

translate_client = boto3.client('translate')


def lambda_handler(event, context):
    body = event.get("body", "{}")
    params = json.loads(body)
    my_text = params.get("text", "something")
    from_lang = params.get("from", "en")
    to_lang = params.get("to", "fr")
    translate_response = {"TranslatedText": {'test': 'response'}}

    print(my_text)

    try:
        translate_response = translate_client.translate_text(
            Text=my_text,
            SourceLanguageCode=from_lang,
            TargetLanguageCode=to_lang
        )
    except Exception as e:
        print("That's exceptional")
        print(e)

    print(translate_response)
    return {
        'statusCode': 200,
        'body': json.dumps(translate_response["TranslatedText"]),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
