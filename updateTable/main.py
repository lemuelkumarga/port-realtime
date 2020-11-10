import globalvars as g
import polygon as p
import dynamodb as ddb

def lambda_handler(event, context):
    
    p.main()
    if g.cache:
        ddb.main()
    
    return "Query executed successfully"


        