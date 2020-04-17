#input file to store file at AWS S3 storage  
import boto3

def lambda_handler(event, context):
	s3 = boto3.resource("s3")
	
	Data=event['data'];
	encoded_string = Data.encode("utf-8")
	
  #specify your bucket name, in my case is "datahello" and the filename that i want is "NewlyCreated.txt" 
	s3.Bucket("datahello").put_object(Key="NewlyCreated.txt",Body=encoded_string)
	
	return "File stored"
    
