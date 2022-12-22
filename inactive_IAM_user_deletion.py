import boto3
import datetime

threshold = int(input('Threshold for inactivity (45-90 days) : '))

if threshold > 45 or threshold < 90:
    pass
else:

    iam = boto3.client('iam')
    
    users = iam.list_users()['Users']
    ##Use when opting for pagination - set marker to the last response value to let the api know the starting point of traversal
    
    #response = [user['UserName'] for user in iam.list_user_tags(UserName='string',Marker='string',MaxItems=123)['Users']]
    
    for user in users:
        try:
            if datetime.datetime.now() - user['PasswordLastUsed'] > threshold:
                iam.delete_user( UserName=user['UserName'])
                print(f'User with Username {user["UserName"]} has been deleted due to inactivity')
        except:
            if datetime.datetime.now() - user['CreateDate'] > threshold :
                iam.delete_user( UserName=user['UserName'])
                print(f'User with Username f{user["UserName"]} has been deleted due to inactivity')
