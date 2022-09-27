from dotenv import load_dotenv
import os
load_dotenv()

def configure():
    load_dotenv()


def get_aws_access_key_id():
    return os.environ["Access_key_ID"]


def get_aws_secret_access_key():
    return os.environ["Secret_access_key"]


def get_mongodb_url():
    return os.environ["mongodb_url"]
