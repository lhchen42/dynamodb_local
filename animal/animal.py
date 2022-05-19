import json
import os
import boto3

def lambda_handler(event, context):

    table_name = os.environ["TABLENAME"]
    aws_environment = os.environ['AWSENV']
    dev_environment = os.environ['DEVENV']

    # Check if executing locally or on AWS, and configure DynamoDB connection accordingly.
    if aws_environment == "AWS_SAM_LOCAL":
        # SAM LOCAL
        if dev_environment == "OSX":
            # Environment ins Mac OSX
            # animal_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000/").Table(table_name)
            animal_table = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000/").Table(table_name)
        elif dev_environment == "Windows":
            # Environment is Windows
            # animal_table = boto3.resource('dynamodb', endpoint_url="http://docker.for.windows.localhost:8000/").Table(table_name)
            animal_table = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000/").Table(table_name)
        else:
            # Environment is Linux
            animal_table = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000").Table(table_name)
    else:
        # AWS
        animal_table = boto3.resource('dynamodb').Table(table_name)

    httpMethod = event["httpMethod"]

    responseBody = {}
    if httpMethod == "GET":
        # return table summary
        responseBody = {
            "tableName": animal_table.name,
            "count": animal_table.item_count
        }
    elif httpMethod == "POST":
        # add an item to table
        try:
            import uuid
            requestBody = json.loads(event["body"])
            requestBody['id'] = str(uuid.uuid4())
            animal_table.put_item(
                Item=requestBody
            )
            responseBody = {
                "tableName": animal_table.name,
                "count": animal_table.item_count,
                "requestBody": requestBody
            }
            print(responseBody)
        except Exception as e:
            responseBody = {
                "message": str(e)
            }
    else:
        responseBody = {
            "message": "Unsupported HttpMethod"
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps(responseBody),
    }
