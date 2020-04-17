import boto3
import tarfile
from io import BytesIO

def lambda_handler(event,context):
	
	s3=boto3.client('s3') #Connection to s3
	bucket ='datahello' #Target bucket
	key = '367639164540-NER-67a48910ac1ebb6de5b058ec8343a32d/output/output.tar.gz' #Target location
	response = s3.get_object(Bucket=bucket, Key=key) #Get the file from S3 storage
	input_tar_content = response['Body'].read() #Read the content of the file
	
	#Read the file content of the zipped file and extract it
	with tarfile.open(fileobj = BytesIO(input_tar_content)) as tar:
		for tar_resource in tar:
			if (tar_resource.isfile()):
				bytes_content = tar.extractfile(tar_resource).read() #Read the content of extracted file
				#Upload a new file in a new S3 path
				s3.upload_fileobj(BytesIO(bytes_content), Bucket = bucket, Key = "NewOutput.txt") 
				
				
