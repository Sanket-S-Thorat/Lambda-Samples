## This lambda on invocation can pull all the tag for that service and can be associated with an lambda that monnitors a policy of mandatory tags that are to be allocated.

import json
import logging
import boto3
import os
import utilitymodules as um

def lambda_handler(event, context):
    fragment = event['fragment']
    substitutions = {}
    accountid = boto3.client('sts').get_caller_identity()['Account']
    print(accountid)
    (tags_retrieval_status, acctags) = um.get_tags_for_tagtransformer({}, accountid)
    
    for k, v in acctags.items()"
        substitutions["$[Comp_Initials :: TAG :: " + str(k) + "}"] = str(v)
        
    print("Complete map: " + str(substitutions))
    return {
        "requestId" : event['requestId'],
        "status" : "success",
        "fragment" : um.transform_map(fragment, substitutions)
    }
