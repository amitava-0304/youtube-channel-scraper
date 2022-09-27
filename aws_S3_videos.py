import os
import shutil
import aws_S3_bucket
from urllib.parse import urlparse



def reset_directory():
    target_path = './videos'
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)

def handle_videos(url):
    conn_string = aws_S3_bucket.create_connection()
    aws_S3_bucket.download_videos(url)
    id = urlparse(url).query[2::]
    path = os.path.join(os.path.dirname(__file__), 'videos', f"{id}.mp4").replace('\\', '/')
    # Then we will upload video
    with open(path, 'rb') as file:
        aws_S3_bucket.upload_video(conn_string, file, 'youtube-vedios', f"{id}.mp4")
    try:
        return aws_S3_bucket.create_presigned_url(conn_string, 'youtube-vedios', f"{id}.mp4")
    except Exception as e:
        print(f"Some Exception occurred {e}")


