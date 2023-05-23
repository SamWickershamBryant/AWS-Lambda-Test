from chalice import Chalice, BadRequestError
import boto3

app = Chalice(app_name='metallicbands')

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('metalliclebands')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/metalbands')
def listAll():
    response = table.scan()
    if response.get('Items'):
        return response['Items']
        
    else:
        return {"error":"no items"}

@app.route('/delete/{id}')
def delete(id):
    response = table.get_item(
        Key={
            'id': id
        }
    )
    table.delete_item(
        Key={
            'id': id
        }
    )
    return response["Item"]

@app.route('/query/{attribute}/{value}', methods=['GET'])
def query(attribute, value):


    if attribute not in ['formed', 'origin', 'split']:
        raise BadRequestError(f'Invalid attribute: {attribute}')

    # Using scan operation because DynamoDB only allows querying on keys
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr(attribute).eq(value)
    )
    return response['Items']

@app.route('/add', methods=['POST'])
def add():
    body = app.current_request.json_body
    table.put_item(Item=body)
    return {"status":"SUCCESS"}

@app.route('/update', methods=['PUT'])
def replace():
    body = app.current_request.json_body

    if not body:
        raise BadRequestError("Must provide item body to replace")

   

    table.put_item(Item=body)
    return {'status': 'Item replaced'}




# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
