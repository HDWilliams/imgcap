import os
import logging
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError
from flask import flash

def upload_to_aws(file, s3_file, bucket = os.getenv('BUCKET')):
    """ add images to aws (s3) CDN, 
    Args:
        file: image data
        s3_file: name of file to save in s3
        bucket: name of bucket used on s3
    """
    #create client specific to aws s3
    s3 = boto3.client('s3')
    image_file_bytes = BytesIO(file)
    #ADD DATETIME MARKER TO MAKE IMAGE NAMES UNIQUE
    try:
        s3.put_object(Bucket=bucket, Key=s3_file, Body=image_file_bytes )
        return f"https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_file}"
    except FileNotFoundError as e:
        logging.exception(e)
        print("The file was not found")
        return False
    except NoCredentialsError as e:
        logging.exception(e)
        print("Credentials not available")
        return False

def delete_from_aws(key, bucket = os.getenv('BUCKET')):
    """ 
        Args:
            key (str): file name in s3
            bucket (str): bucket on s3 in which image stored

        returns: None
    """
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except FileNotFoundError:
        print("The file was not found")
        logging.exception(e)
        return False
    
    except NoCredentialsError:
        print("Credentials not available")
        logging.exception(e)
        return False
    except Exception as e:
        flash('Delete operation has succeed at database level but failed to delete from CDN. No further action needed')
        logging.exception(e)
        return False
    return True
