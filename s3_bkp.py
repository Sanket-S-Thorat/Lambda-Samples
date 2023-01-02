import boto3

# Set the name of the S3 bucket and the prefix for the backup objects
bucket_name = input('Bucket Name : ')
prefix = 'backup/'

# Create an S3 client
s3_client = boto3.client('s3')

# Get a list of all objects in the bucket
objects = s3_client.list_objects(Bucket=bucket_name)

# Iterate through the list of objects and create a copy of each object
for obj in objects['Contents']:
    key = obj['Key']
    s3_client.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': key}, Key=prefix + key)
