import json
import boto3
from datetime import datetime, timezone, timedelta
from dateutil import tz

# Get DynamoDB resource
tbl = boto3.resource('dynamodb').Table("raw_data")

cur_time=""
output={}

# Get last updated item
def get_ts(portfolio):
    out_q = tbl.query(
                IndexName="portfolio-ts-index",
                ScanIndexForward=False,
                Limit=60,
                ProjectionExpression="portfolio,ts,ts_ret",
                KeyConditionExpression="portfolio = :k and ts <= :t",
                ExpressionAttributeValues={
                    ':k': portfolio,
                    ':t': cur_time
                })['Items']
    for i in out_q:
        ts = i['ts']
        if ts not in output:
            output[ts] = {}
        output[ts][portfolio] = str(i['ts_ret'])

def lambda_handler(event, context):
    
    # Get latest time (with 30 minute lag)
    global cur_time
    cur_time = datetime.now().replace(tzinfo=tz.tzutc()) \
                .astimezone(tz=tz.gettz('America/New_York'))-timedelta(minutes=30)
    cur_time = cur_time.strftime('%Y-%m-%d %H:%M:%S')

    get_ts('VTI')
    get_ts('VXUS')
    
    str_out = 'Time,VTI,VXUS\n'
    for k in list(sorted(output.keys()))[-60:]:

        utc_time = datetime.strptime(k,'%Y-%m-%d %H:%M:%S')
        #utc_epoch = "{:.0f}000".format(utc_time.timestamp())
        
        utc_format = utc_time.replace(tzinfo=tz.gettz('America/New_York')).astimezone(tz=tz.tzutc()).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        str_out += ','.join([utc_format, output[k]['VTI'], output[k]['VXUS']]) + '\n'
    
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body': str_out
    }

