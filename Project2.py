import streamlit as st
import boto3
import uuid
import json
from credentials import aws_access_key_id, aws_secret_access_key, region_name

#SECURITY CREDENTIALS
aws_access_key_id = aws_access_key_id
aws_secret_access_key = aws_secret_access_key
region_name = region_name

#AWS LAMBDA INTEGRATION
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)
dynamodb = boto3.resource(
    'dynamodb', 
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

#Interface creation
st.title('SnapGram')

st.sidebar.header("Home")
image=st.sidebar.file_uploader("Drop your image here",accept_multiple_files=True)
text=st.sidebar.text_area("write caption.....")
button1=st.sidebar.button('POST')
button2=st.sidebar.button('SHOW TRENDING HASHTAGS')


post_data = {
        'post_id': str(uuid.uuid4()),
        'post': text
    }
var1=json.dumps(post_data)
#st.write(var1)

# Button to submit the post
if button1:                
    st.image(image)
    st.write(text)

# Process the post and hashtags
    response=lambda_client.invoke(
        FunctionName='Snapgram',
        Payload=var1
    )
#Extracting hashtags from post and inserting into Dynamodb  
    hash_list = []
    split_list=var1.split("\"")
    # st.write(split_list)
    split_list_hash=(split_list[7].split(" "))
    for word in split_list_hash:
       if word[0]=='#':
          hash_list.append(word[1:])
    table=dynamodb.Table('Trending_Hashtag')        
    for hashtag in hash_list:
        
        table.put_item(Item={'Post_id':split_list[3],'Hashtag': hashtag}) 

#Retrieval of hashtags from table
def getColumn1Items():
    table = dynamodb.Table('Trending_Hashtag')
    response = table.scan()
    return ([i['Hashtag'] for i in response['Items']])

if button2:
    st.write(getColumn1Items())






  