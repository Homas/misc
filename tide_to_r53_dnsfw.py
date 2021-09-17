#(c) Vadim Pavlov
#2021-09-17
#lambda function to improt IoCs from TIDE to AWS Route 53 DNS Firewall
import json, os, urllib3, logging, boto3
from pprint import pprint
logging.basicConfig(level = logging.INFO, force=True)
search = os.environ['SEARCH']
APIkey = os.environ['CSP_API_KEY']
dnsFWListId = os.environ['DNSFW_LISTID']
s3Bucket = os.environ['S3BUCKET']
s3File = os.environ['S3FILE']
s3URL="s3://"+s3Bucket+"/"+s3File
print (s3URL)
baseURL = 'https://csp.infoblox.com'
authH = {'Authorization':'Token token='+APIkey}
tideREST = urllib3.PoolManager(timeout=30.0)

s3 = boto3.client('s3')
r53 = boto3.client('route53resolver')

def lambda_handler(event, context):
    # TODO implement

    try:
        r = tideREST.request('GET', baseURL+search, headers=authH)
        if (r.status==200):
            #print("ioc:", r.data[5:])
            s3r = s3.put_object(
                Body=r.data[5:],
                Bucket=s3Bucket,
                Key=s3File,
            )
            ###add error handling
            r53r=r53.import_firewall_domains(
                FirewallDomainListId=dnsFWListId,
                Operation='REPLACE',
                DomainFileUrl=s3URL
            )
            ###add error handling            
            pprint(r53r)

    except Exception as e:
        print("send(..) failed executing tideREST.request(..):", e)


    
    #+Pull TI
    #+Remove header
    #+Save it on S3
    #Push the update to R53 DNSFW
    #https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ImportFirewallDomains.html
    
    return {
        'statusCode': 200,
        'body': 'Life is good'
    }
