import boto3

##Get WAF Version:
version = input('WAF Version (regional/V2) : ')
waf_v = 'wafv2' 
if version.lower()=='regional':waf_v = 'waf-regional'

##Get WEB ACL ARN: 
acl =input('ARN of WEB ACL : ')

##Get the region
region = input('Region :')

client = boto3.client('apigateway')
clientV2 = boto3.client('apigatewayv2')

waf = boto3.client(waf_v)

##List all API Ids
apis = [api['id'] for api in client.get_rest_apis()['items']]
rest_apis = [api['ApiId'] for api in clientV2.get_apis()['Items']]
print(apis, rest_apis)

for api in apis:
    ##get all stages
    stages = [stage['stageName'] for stage in client.get_stages(restApiId = api)['item']]
    print(client.get_stages(restApiId = api))
    for stage in stages:
        
        arn = f'arn:aws:apigateway:{region}::/restapis/ {api}/stages/{stage}'
        
        ##Connect to webacls
        waf.associate_web_acl(WebACLArn=f'{acl}', ResourceArn=f'{arn}')

for rest_api in rest_apis:
    ##get all stages
    stages = [stage['StageName'] for stage in clientV2.get_stages(ApiId = rest_api)['Items']]
    print(stages)
    
    for stage in stages:
        
        arn = f'arn:aws:apigateway: {region}::/restapis/ {rest_api}/stages/{stage}'
        
        ##Connect to webacls
        waf.associate_web_acl(WebACLArn=f'{acl}', ResourceArn=f'{arn}')
