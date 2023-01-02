import boto3
import datetime

# Set the rotation interval in days
rotation_interval = 45

# Create an IAM client
iam_client = boto3.client('iam')

# Get a list of all IAM users in the account
response = iam_client.list_users()

# Iterate through the list of users
for user in response['Users']:
    user_name = user['UserName']
    
    # Get a list of the user's access keys
    access_keys = iam_client.list_access_keys(UserName=user_name)
    
    # If the user has only one access key, skip to the next user
    if len(access_keys['AccessKeyMetadata']) <= 1:
        continue
    
    # Get the creation date of the oldest access key
    oldest_key_creation_date = access_keys['AccessKeyMetadata'][-1]['CreateDate']
    
    # Calculate the age of the oldest access key
    age = (datetime.datetime.now(datetime.timezone.utc) - oldest_key_creation_date).days
    
    # If the age of the oldest access key is greater than the rotation interval, rotate the access keys
    if age > rotation_interval:
        # Delete all but the most recently created access key
        for access_key in access_keys['AccessKeyMetadata'][:-1]:
            iam_client.delete_access_key(UserName=user_name, AccessKeyId=access_key['AccessKeyId'])

        # Create a new access key
        new_access_key = iam_client.create_access_key(UserName=user_name)

        # Delete the old access key (Primary access key) if needed.
        #iam_client.delete_access_key(UserName=user_name, AccessKeyId=access_keys['AccessKeyMetadata'][-1]['AccessKeyId'])
