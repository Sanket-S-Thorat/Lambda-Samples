import boto3

client = boto3.client('lambda')

##Get KMS Key Arn:
arn = input('KMS Key ARN : ')

##get all Lambdas
func = [function['FunctionName'] for function in client.list_functions()['Functions']]

for fun in func:
    config = client.update_function_configuration(FunctionName = fun, KMSKeyArn=arn)
