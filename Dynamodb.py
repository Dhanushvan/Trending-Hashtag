import boto3
import Project2

aws_access_key_id = 'AKIAZQ3DNUR33CR5UKHQ'
aws_secret_access_key = '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'
region_name = 'ap-south-1'

dynamodb = boto3.resource(
    'dynamodb', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

table_name = 'Trending_Hashtag'
table_schema = [
    {
        'AttributeName': 'Post_id',
        'KeyType' : 'HASH'          
    },
    {
        'AttributeName': 'Hashtag',
        'KeyType': 'RANGE'
    }
]

provisioned_throughput = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
}


response = dynamodb.create_table(
    TableName=table_name,
    AttributeDefinitions=[
        {
            'AttributeName': 'Post_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'Hashtag',
            'AttributeType': 'S'
        }
    ],
KeySchema=table_schema,
ProvisionedThroughput=provisioned_throughput
)
