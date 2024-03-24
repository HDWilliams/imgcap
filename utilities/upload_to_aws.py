import boto3
from botocore.exceptions import NoCredentialsError
import os
from io import BytesIO

""" Upload a file to s3 bucket for image storage using AWS
    credentials for s3 handled by env variables
    returns valid object access url, or returns false

    FURTHER STEP COULD BE TO USE PRESIGNED URL
"""

def upload_to_aws(file, s3_file, bucket = os.getenv('BUCKET')):
    #create client specific to aws s3
    s3 = boto3.client('s3')
    image_file_bytes = BytesIO(file)

    try:
        s3.put_object(Bucket=bucket, Key=s3_file, Body=image_file_bytes )
        print("Upload Successful")
        return f"https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_file}"
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
