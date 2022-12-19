import boto3

sqs = boto3.client('sqs')

keyId = input('KS KeyId for SQS Encryption : ')
keyReusePeriod = input('Key Reuse Period (60 - 500 (seconds)) : ')
all_sqs = [queue for queue in sqs.list_queues()['QueueUrls']]

for queue in all_sqs:
    try:
        sqs.get_queue_attributes( QueueUrl=f'{queue}', AttributeNames=['KmsMasterKeyId'])['Attributes']
        continue
    except :
        print(queue)
        sqs.set_queue_attributes( QueueUrl=f'{queue}',Attributes={'KmsMasterKeyId':f'{keyId}', 'KmsDataKeyReusePeriodSeconds':f'{keyReusePeriod}'})
