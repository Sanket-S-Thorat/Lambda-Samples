import boto3

keyId = input('KMS Key Id to be used for encryption : ')
smgr = boto3.client('secretsmanager')

secrets = [secret['ARN'] for secret in smgr.list_secrets()['SecretList']]

for secret in secrets:
    response = smgr.rotate_secret(SecretId=secret,RotationRules={'AutomaticallyAfterDays': 90},RotateImmediately=False)
    try:
        smgr.describe_secret(SecretId= secret)['KmsKeyId']
    except:
        smgr.update_secret(KmsKeyId=f'{keyId}')
    
