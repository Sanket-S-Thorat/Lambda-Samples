import boto3

keyId = input('KMS KeyId : ')

dynamodb = boto3.client('dynamodb')
ddbs = dynamodb.list_tables()['TableNames']

##Do not alter the sequence of update else can throw an still in update error.

## Enabling continuous backups
for ddb in ddbs:
    dynamodb.update_continuous_backups(TableName = ddb, PointInTimeRecoverySpecification={'PointInTimeRecoveryEnabled' : True})

## Encrypting the DynamoDbs
for ddb in ddbs:
    try:
        descp = dynamodb.describe_table(TableName = ddb)['SSEDescription']
        if descp['SSEType'] == 'AES256':
            dynamodb.update_table(TableName = ddb, SSESpecification={'Enabled': True, 'SSEType': 'KMS', 'KMSMasterKeyId': f'{keyId}'})
    except:
        dynamodb.update_table(TableName = ddb, SSESpecification={'Enabled': True, 'SSEType': 'KMS', 'KMSMasterKeyId': f'{keyId}'})
