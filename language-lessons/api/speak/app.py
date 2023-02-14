import json
import boto3
import os
import hashlib
from contextlib import closing


def get_voice_for_language(language):
    voices = {"fr": "Lea", "en": "Salli", "de": "Vicki", "es": "Lupe"}
    return voices.get(language, "Salli")


def lambda_handler(event, context):
    # This function will accept text and return an audio file containing that text
    # params are text and language

    body = event.get("body", "{}")

    params = json.loads(body)

    text = params.get("text", "something")
    language = params.get("language", "en")
    voice = get_voice_for_language(language)

    raw_lookup_id = voice + ":" + text
    hashed_id = hashlib.sha256(raw_lookup_id.encode('UTF-8')).hexdigest()
    print(hashed_id)

    bucket_id = "rickslearning.com.pollyfiles"

    recording_id = hashed_id + ".mp3"

    # Lets look to see if the file already exists, and if so we don't need to transcribe it
    try:
        s3 = boto3.client('s3')
        my_file = s3.get_object(Bucket=bucket_id, Key=recording_id)
        print("reading from cache")
    except:
        polly = boto3.client('polly')

        response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=text,
            VoiceId=voice,
        )

        audio = response["AudioStream"]

        with closing(audio) as stream:
            output = os.path.join("/tmp/", recording_id)
            with open(output, "wb") as file:
                file.write(stream.read())

        s3.upload_file('/tmp/' + recording_id, bucket_id, recording_id)

    file_url = "https://s3.amazonaws.com/rickslearning.com.pollyfiles/" + recording_id

    return {
        'statusCode': 200,
        'body': file_url,
        'headers': {
            'Content-Type': 'text/json',
            'Access-Control-Allow-Origin': '*',
        },
    }
