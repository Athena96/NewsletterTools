import webbrowser
import boto3
import os
from lib.newsletter import Newsletter
from dotenv import load_dotenv

'''
# Usage
python3 src/publish.py

# Description
1. The script loads credentials from environment variables.
2. Newsletter dates and file name are defined.
3. A Lambda client is created and the newsletter sender function is updated to enable actual sending of emails.
4. The generate newsletter function is updated to disable sending test emails.
5. A S3 client is created using the provided access key and secret key.
6. The newsletter file is uploaded to an S3 bucket.
7. The script prompts the user to confirm uploading the newsletter file to S3.
8. If the user confirms, the file is uploaded to the S3 bucket.
9. The script opens Gmail in a Chrome browser.
10. The script generates a console sign-in URL for AWS SES and opens it in a web browser.
'''
load_dotenv()

region = os.getenv('aws_region')

def get_user_input(prompt):
    user_input = input(prompt).strip().lower()
    while user_input not in ['y', 'n']:
        print("Invalid input. Please enter 'y' or 'n'.")
        user_input = input(prompt).strip().lower()
    return user_input

# load creds
access_key_id = os.getenv('access_key_id')
secret_access_key = os.getenv('secret_access_key')

# define newsletter dates and file name
newsletter = Newsletter()

# create lambda client
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

# update the generate newsletter function to SEND_TEST = false
newsletter_generator_function_name = os.getenv('newsletter_generator_function_name')
api_id = os.getenv('api_id')
subscriber_table = os.getenv('subscriber_table')
sender_email = os.getenv('sender_email')
queue_name = os.getenv('queue_name')
newsletter_generator_environment_variables = {
    "API_ID_PARAM_NAME": api_id,
    "BATCH_SIZE": "1",
    "SUB_TABLE_NAME": subscriber_table,
    "SEND_TEST": "false",
    "QUEUE_NAME": queue_name
}
lambda_client.update_function_configuration(
    FunctionName=newsletter_generator_function_name,
    Environment={
        'Variables': newsletter_generator_environment_variables
    }
)
print(f"Updated Lambda function '{newsletter_generator_function_name}' to SEND_TEST =false")


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

user_response = get_user_input(f"Do you want to upload the newsletter file {newsletter.filename + '.html'} to s3? THIS WILL SEND THE EMAIL TO ALL SUBSCRUBERS (y/n): ")
print("User response:", user_response)

if user_response != 'y':
    print("Exiting...")
    exit()

s3_client.upload_file(file_path, bucket_name, key)
print(f"Uploaded file '{file_path}' to S3 bucket '{bucket_name}'.")

# open Gmail in chrome
print(f"Opening newsletter in gmail...")
webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

# open SES dashboard in chrome
# Create a session using the provided access key, secret key, and region
session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name=region)

# Generate a console sign-in URL
sts_client = session.client('sts')
response = sts_client.get_session_token()
credentials = response['Credentials']
console_url = f"https://console.aws.amazon.com/console/home?region={session.region_name}#awsSignInModal:accessKey={credentials['AccessKeyId']}&secretKey={credentials['SecretAccessKey']}&sessionToken={credentials['SessionToken']}"

# Open the console URL in a web browser
webbrowser.open(console_url)
webbrowser.open("https://us-west-2.console.aws.amazon.com/ses/home?region=us-west-2#/vdm/dashboard")
