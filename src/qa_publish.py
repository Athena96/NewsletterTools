import time
import webbrowser
import boto3
import os
from lib.newsletter import Newsletter
from dotenv import load_dotenv


'''
# Usage
python3 src/qa_publish.py

# Description
1. The script loads credentials from the environment variables.
2. It defines the dates and file name for the newsletter.
3. A Lambda client is created using the AWS access key and secret access key.
4. The newsletter sender function is updated to enable actual sending of emails.
5. The generate newsletter function is updated to set the sender email for testing.
6. A S3 client is created using the AWS access key and secret access key.
7. The newsletter file is uploaded to an S3 bucket.
8. The script opens Gmail in a Chrome browser.
9. It pauses execution for 10 seconds.
10. The newsletter file is deleted from the S3 bucket.
'''

# load creds
load_dotenv()
access_key_id = os.getenv('access_key_id')
secret_access_key = os.getenv('secret_access_key')

# define newsletter dates and file name
newsletter = Newsletter()

# create lambda client
region = os.getenv('aws_region')
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region
)

# update the newsletter sender function to ACTUALLY_SEND_EMAILS = true
bucket_name = os.getenv('bucket_name')
newsletter_sender_function_name = os.getenv('newsletter_sender_function_name')
newsletter_sender_environment_variables = {
    "ACTUALLY_SEND_EMAILS": "true",
    "BUCKET_NAME": bucket_name
}
lambda_client.update_function_configuration(
    FunctionName=newsletter_sender_function_name,
    Environment={
        'Variables': newsletter_sender_environment_variables
    }
)
print(f"Updated Lambda function '{newsletter_sender_function_name}' to ACTUALLY_SEND_EMAILS = true.")

# update the generate newsletter function to SEND_TEST = sender_email
newsletter_generator_function_name = os.getenv('newsletter_generator_function_name')
api_id = os.getenv('api_id')
subscriber_table = os.getenv('subscriber_table')
sender_email = os.getenv('sender_email')
queue_name = os.getenv('queue_name')
newsletter_generator_environment_variables = {
    "API_ID_PARAM_NAME": api_id,
    "BATCH_SIZE": "1",
    "SUB_TABLE_NAME": subscriber_table,
    "SEND_TEST": sender_email,
    "QUEUE_NAME": queue_name
}
lambda_client.update_function_configuration(
    FunctionName=newsletter_generator_function_name,
    Environment={
        'Variables': newsletter_generator_environment_variables
    }
)
print(f"Updated Lambda function '{newsletter_generator_function_name}' to SEND_TEST = '{sender_email}'")

# define s3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region
)

# Upload the file to S3
newsletter_local_dir = os.getenv('newsletter_local_dir')
file_path = newsletter_local_dir + newsletter.filename + '.html'
key = newsletter.filename + '.html'
s3_client.upload_file(file_path, bucket_name, key)
print(f"Uploaded file '{file_path}' to S3 bucket '{bucket_name}'.")

# open Gmail in chrome
print(f"Opening newsletter in gmail...")
webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

# sleep 10s
print(f"Sleeping for 10s...")
time.sleep(10)

# delete newsletter file from s3
s3_client.delete_object(Bucket=bucket_name, Key=key)
print(f"Deleted file '{key}' from S3 bucket '{bucket_name}'.")