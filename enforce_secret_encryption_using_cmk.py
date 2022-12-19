import boto3

keyId = input('KMS Key Id to be used for encryption : ')

smgr = boto3.client('secretsmanager')

secrets = [secret['ARN'] for secret in smgr.list_secrets()['SecretList']]

for secret in secrets:
    smgr.update_secret(KmsKeyId=f'{keyId}')

