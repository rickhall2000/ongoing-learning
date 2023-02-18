import json
import base64
import boto3
import uuid
import time
import urllib.request

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

def lambda_handler(event, context):

    body = json.loads(event['body'])
    mp3_file = body['file']

    bad_str = "data:audio/mp3;base64,"

    short_str = mp3_file[len(bad_str):]

    mp3_binary = base64.b64decode(short_str)

    bucket_name = 'rickslearning.audiorecordings'

    object_key = uuid.uuid4()
    object_key = str(object_key)
    s3_filename = object_key + ".mp3"


    try:
        s3.put_object(Body=mp3_binary, Bucket=bucket_name, Key=s3_filename)
    except Exception as e:
        print("putting to s3 failed")
        print(e)


    # Set up the transcription job
    job_name = object_key
    job_uri = f's3://{bucket_name}/{s3_filename}'
    media_format = 'mp3'

    language_code = body['language']
    print(language_code)
#    language_code = "en-US"

    transcribe_response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=media_format,
        LanguageCode=language_code
    )

    transcription_job = transcribe_response['TranscriptionJob']
    transcription_job_name = transcription_job['TranscriptionJobName']

    response = transcribe.get_transcription_job(
        TranscriptionJobName=transcription_job_name
    )
    status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    while status == 'IN_PROGRESS':
        time.sleep(2.0)
        print("polling again")
        response = transcribe.get_transcription_job(
            TranscriptionJobName=transcription_job_name
        )
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]

    result_file = response["TranscriptionJob"]['Transcript']["TranscriptFileUri"]

    req = urllib.request.Request(result_file)
    resp = urllib.request.urlopen(req)
    blah = resp.read()
    # convert blah to json 
    my_json = blah.decode('utf8').replace("'", '"')
#    my_json = '{"jobName":"29533a64-655d-41bd-9d02-cca87768aab9","accountId":"526018917548","results":{"transcripts":[{"transcript":"Tell me what you hear."}],"items":[{"start_time":"0.21","end_time":"0.65","alternatives":[{"confidence":"1.0","content":"Tell"}],"type":"pronunciation"},{"start_time":"0.65","end_time":"0.87","alternatives":[{"confidence":"1.0","content":"me"}],"type":"pronunciation"},{"start_time":"0.87","end_time":"1.14","alternatives":[{"confidence":"1.0","content":"what"}],"type":"pronunciation"},{"start_time":"1.14","end_time":"1.34","alternatives":[{"confidence":"0.9995","content":"you"}],"type":"pronunciation"},{"start_time":"1.34","end_time":"1.92","alternatives":[{"confidence":"0.9102","content":"hear"}],"type":"pronunciation"},{"alternatives":[{"confidence":"0.0","content":"."}],"type":"punctuation"}]},"status":"COMPLETED"}'

    # extract the transcript
    transcript = json.loads(my_json).get("results").get("transcripts")[0].get("transcript")
    print(transcript)

    return {
        'statusCode': 200,
        'body': json.dumps(transcript),
        'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                   }
    }

