from decimal import Decimal
from datetime import datetime
from datetime import timedelta
import botocore
import boto3

import globalvars as g

# Get DynamoDB resource
tbl = boto3.resource('dynamodb').Table("raw_data")

# Insert stock data into the database
def insert_entry(portfolio, time, val):
    
    has_existing_entry = True;
    
    # Get yesterday's values for the particular time
    try:
        vals = tbl.get_item(
            Key={
                'portfolio': portfolio,
                'time': time
            },
            AttributesToGet=[ 'ts_val' ]
        )['Item']
        yest_val = float(vals['ts_val'])
    except KeyError:
        has_existing_entry = False
    
    # Create item if does not exist
    if (not has_existing_entry):
        tbl.put_item(
            Item={
                'portfolio' : portfolio,
                'time': time,
                'ts': g.cur_dt + ' ' + time,
                'ts_val': Decimal(str(val)),
                'ts_ret': Decimal(str(0.0))
            })
        
        if (g.debug):
            print(portfolio + "," + time + " item created.")
    # Otherwise, update the item
    else:
        tbl.update_item(
            Key={
                'portfolio' : portfolio,
                'time' : time
            },
            UpdateExpression="SET ts = :t, ts_val = :v, ts_ret = :r",
            ExpressionAttributeValues={
                ':v': Decimal(str(val)),
                ':r': Decimal(str((val - yest_val) / yest_val)),
                ':t': g.cur_dt + ' ' + time
            })
        
        if (g.debug):
            print(portfolio + "," + time + " updated to latest date (" + g.cur_dt + ").")

# Generates last known time and stock prices
def upload_params():
    
    # Get last updated item
    def get_last_modified_item(portfolio):
        return tbl.query(
                    IndexName="portfolio-ts-index",
                    ScanIndexForward=False,
                    Limit=1,
                    ProjectionExpression="portfolio,ts,ts_val",
                    KeyConditionExpression="portfolio = :k",
                    ExpressionAttributeValues={
                        ':k': portfolio
                    })['Items'][0]
    
    #Get the last row that was modified
    last_mod = {}
    for i in g.tickers:
        last_mod[i] = get_last_modified_item(i)
    
    if (g.debug):
        map(lambda x : print(x[0] + " price @ " + x[1]["ts"] + ": " + x[1]["ts_val"]), last_mod.items())

    return [last_mod[g.tickers[0]]["ts"], { k : float(v['ts_val']) for k, v in last_mod.items() }]

# Generates a list of times to be updated
def upload_intervals(start_ts):
    
    start_dt, start_time = start_ts.split(' ')
    
    end_time = max(g.cache.keys())
    
    start_dt, end_dt = map(lambda x : datetime.strptime(x,'%H:%M:%S'),[start_time, end_time])
    min_diff = int((end_dt - start_dt).total_seconds() / 2)
    
    return [(start_dt + timedelta(seconds=2*(x+1))).strftime('%H:%M:%S') \
                for x in range(max(min_diff,0))]
    
# Main function to store prices into database
def main():
    
    start_ts, cur_prices = upload_params()
    
    # If last modified value was previous trading day
    # fast forward to 9:30 am to the current date
    start_dt, start_time = start_ts.split(' ')
    if (start_dt < g.cur_dt):
        start_ts =  g.cur_dt + ' ' + "09:30:00"

    for t in upload_intervals(start_ts): 
        
        if t not in g.cache:
            prices = {}
        else:
            prices = g.cache[t]

        for i in g.tickers:
            # Update current prices
            if i in prices:
                cur_prices[i] = prices[i]
            
            # Insert the current time prices
            insert_entry(i,t, cur_prices[i])

