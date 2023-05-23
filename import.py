import boto3
import csv

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('metalliclebands')



response = table.scan()

# Check if any items were returned
if response.get('Items'):
    first_item = response['Items'][0]  # get the first item
    print(first_item)
else:
    print("No items in DynamoDB table.")