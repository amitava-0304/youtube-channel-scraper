import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from pytube import YouTube
import os
from urllib.parse import urlparse
import setup
def create_connection():
    """Make connection with s3 Bucket
    return: connection string
    """
    # client for S3 Bucket AWS
    try:
        s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id=setup.get_aws_access_key_id(),
                                 aws_secret_access_key=setup.get_aws_secret_access_key(),
                                 config=Config(signature_version='s3v4'),
                                 endpoint_url='https://s3.us-east-2.amazonaws.com')
        return s3_client
    except Exception as e:
        return f"some Error in making connection {e}"


def get_bucket_details(s3_client):
    """return: Return details of S3 Buckets"""
    return s3_client.list_buckets()


# Function for creating URL
def create_presigned_url(s3_client,bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        return None

    # The response contains the presigned URL
    return response


def check_video_exist(s3_client, key):
    try:
        x = s3_client.head_object(Bucket='youtube-vedios', Key=key)
        return x
    except Exception as e:
        return "key not found"


def upload_video(s3_client, Filename, Bucket, Key):
    """Upload file in s3 Bucket"""
    try:
        s3_client.upload_fileobj(Filename, Bucket, Key)

    except Exception as e:
       print(f"some Exception {e}")


def download_videos(url, path='./videos'):
   try:
        yt = YouTube(str(url))
        yt.streams.filter(progressive=True, file_extension='mp4').first().download(output_path=path,filename=f'{urlparse(url).query[2::]}.mp4')

   except Exception as e:
        print("some exception", e)

