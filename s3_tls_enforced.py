import boto3
import json

s3 = boto3.resource('s3')
buckets = [bucket.name for bucket in s3.buckets.all()]

s3_client = boto3.client('s3')
policy_list = []
for bucket in buckets:
    try:
        policy_list.append(json.loads(s3_client.get_bucket_policy(Bucket = bucket)['Policy']))
    except:
        policy_list.append(dict())
        

for policy, bucket in zip(policy_list, buckets):
    secure_transport_policy = {
            "Version":
            "2012-10-17",
            "Statement": [{
                "Effect": "Deny",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:*",
                "Resource": [
                        "arn:aws:s3:::{}/*".format(bucket),
                        "arn:aws:s3:::{}".format(bucket)
                    ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
                },
                {
                    "Effect": "Deny",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": "s3:*",
                    "Resource": [
                        "arn:aws:s3:::{}/*".format(bucket),
                        "arn:aws:s3:::{}".format(bucket)
                    ],
                    "Condition": {
                        "NumericLessThan": {
                            "s3:TlsVersion": "1.2"
                        }
                    }
                }
            ]}
    if bool(policy):
        
        policy['Statement'] += secure_transport_policy['Statement']
        s3_client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
        
    else:
        s3_client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(secure_transport_policy))
        
    response = s3_client.put_public_access_block(
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
        },
    Bucket = bucket
    )
