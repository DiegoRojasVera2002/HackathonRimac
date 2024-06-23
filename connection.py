import boto3
from dotenv import load_dotenv
from os import getenv

load_dotenv()

aws_access_key_id = getenv('AWS_ACCESS_KEY_ID_SNS')
aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY_SNS")
aws_region = getenv("AWS_REGION_SNS")


sns_client = boto3.client("sns",
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)