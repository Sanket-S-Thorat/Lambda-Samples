import boto3

# Set the password reset time in days
password_reset_time = 30

# Create an IAM client
iam_client = boto3.client('iam')

# Get the current password policy
password_policy = iam_client.get_account_password_policy()

# Set the password expiration to 30 days
password_policy['PasswordPolicy']['ExpirePasswords'] = True
password_policy['PasswordPolicy']['MaxPasswordAge'] = password_reset_time

# Update the password policy
iam_client.update_account_password_policy(**password_policy)

# Get a list of all IAM users
response = iam_client.list_users()

# Iterate through the list of users and update their login profiles
for user in response['Users']:
    user_name = user['UserName']
    iam_client.update_login_profile(UserName=user_name, PasswordResetRequired=True)
