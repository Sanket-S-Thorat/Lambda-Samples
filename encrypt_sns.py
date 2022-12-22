import boto3

keyId = input('KMS KeyId : ')

sns = boto3.client('sns')
topics = [topic['TopicArn'] for topic in sns.list_topics()['Topics']]

for topic in topics:
    try:
        sns.get_topic_attributes(TopicArn=topic)['Attributes']['KmsMasterKeyId']
    except:
        sns.set_topic_attributes( TopicArn=topic, AttributeName='KmsMasterKeyId', AttributeValue=keyId)
        print(topic)
