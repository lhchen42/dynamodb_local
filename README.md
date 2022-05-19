# dynamodb_local

## How to setup dynamodb local

You can create a dynamodb locally with following command

```bash
docker run -p 8000:8000 amazon/dynamodb-local
```

This will pull the image from the docker-hub and run dynamodb local at port 8000

## Create Table

The dynamodb local do not have any table right now. You can check it with command below

```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

One method to create a table is using aws cli. Beside this, we can also use write a python script. Refer to `util.py` in the Unittest Doc.

```bash
aws dynamodb create-table --cli-input-json file://dummyTable/animalTable.json --endpoint-url http://localhost:8000
```

Where endpoint url `http://localhost:8000` is where dynamodb local hosted

## Run the code locally

```bash
sam local start-api -t --env-vars env/env.json