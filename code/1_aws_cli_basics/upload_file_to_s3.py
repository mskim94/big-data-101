import boto3
import botocore
import os


# create and check bucket
s3 = boto3.client('s3', region_name="ap-southeast-1")
response = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]

if 'bigdata-msk' not in buckets:
    response = s3.create_bucket(
        Bucket='bigdata-msk',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-1'
            }
        )
else:
    print('''bigdata-msk's name already exists''')


# compare vpc.log with new_vpc.log
with open("new_vpc.log", 'r', encoding="utf=8") as new_vpc_log:
    new_line = new_vpc_log.readlines()
    new_line  # 새로운 log

if 'old_vpc.log' in os.listdir():
    with open("old_vpc.log", 'r', encoding="utf-8") as old_vpc_log:
        old_line = old_vpc_log.readlines()
        old_line  # 기존의 log(bucket에서 다운받은)

else:
    BUCKET_NAME = 'bigdata-msk' # replace with your bucket name
    KEY = 'new_vpc.log' # replace with your object key

    s3 = boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'old_vpc.log')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    # download vpc_file
    with open("old_vpc.log", 'a', encoding='utf-8') as f:
        for i in new_line:
            if i not in old_line:
                f.write(i)


# Create an S3 client
s3 = boto3.client('s3')

bucket_name = 'bigdata-msk'
# path = "C:/workspace/big_data/big-data-101/code/1_aws_cli_basics/log"
files = os.listdir('./')
# log_file = os.listdir()
if 'old_vpc.log' in files:
    origin_filename = 'new_vpc.log'
    new_filename = 'new_vpc.log'
    # for filename in files:
    s3.upload_file(origin_filename, bucket_name, new_filename)
