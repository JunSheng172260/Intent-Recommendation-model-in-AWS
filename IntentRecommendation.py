import boto3
import json
import array as arr

def intention(intentList):
    #Set each of the label as a counter and initialize them as 0
    WebAccessControl=0
    Authentication=0
    SelfHealing=0
    Performance=0
    NetworkSecurity=0

    #Increament by 1 if detected the same label in the array
    for counter in intentList:
        if counter=="WEB_ACCESS_CONTROL":
            WebAccessControl+=1
        if counter=="AUTHENTICATION":
            Authentication+=1
        if counter=="PERFORMANCE":
            Authentication+=1
        if counter=="NETWORK_SECURITY":
            NetworkSecurity+=1
       
    intentionList=[WebAccessControl,Authentication,SelfHealing,Performance,NetworkSecurity]
    
    #Return the label with the most frequency
    if(max(intentionList)==WebAccessControl):
        return "WEB_ACCESS_CONTROL"
    elif(max(intentionList)==Authentication):
        return "AUTHENTICATION"
    elif(max(intentionList)==SelfHealing):
        return "SELF_HEALING"
    elif (max(intentionList)==NetworkSecurity):
        return "NetworkSecurity"
    else:
        return "Performance"

def lambda_handler(event, context):
    
    s3=boto3.client('s3') #Connection to S3 service
    
    bucket ='testingset' #Specify the folder that store the file
    key = 'NewOutput.txt' #Specify the filename
    response = s3.get_object(Bucket=bucket, Key=key) #Look for the file by using s3 connection and store the content into response variable 
    
    content = response['Body'].read()
    json_object =json.loads(content)
    obj=json_object['Entities']
    entities=[""]
    entities.clear()
    for person in json_object['Entities']:
        entities.append(person['Type'])
    
    result=intention(entities)
    
    TableName="Intent"
    columnName= 'intent'
    
    #Connection to Dynamo DB
    db=boto3.resource('dynamodb')
    
    #Look for the table and its columm
    table=db.Table(TableName)
    response = table.get_item(Key={columnName:result})
    response_obj=response['Item']
    solution=response_obj['reccomendation']
    print("We have a few reccomendations for your policy, you can perform the solution as follow:")
    counter=1
    for q in solution:
        print(str(counter) + "."+q)
        counter+=1

    return solution;
    
    
