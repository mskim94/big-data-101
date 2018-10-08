import boto3
import logging
from botocore.exceptions import ClientError

# Create EC2 client
ec2 = boto3.client('ec2')
logger = logging.getLogger('vpc')
hdlr = logging.FileHandler('new_vpc.log')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger.addHandler(hdlr)
hdlr.setFormatter(formatter)
logger.setLevel(logging.INFO)

# Delete security group

with open("new_vpc.log", "r", encoding="utf-8") as vpc_log:
    log_list = vpc_log.readlines()

GroupId_list = []

for i in log_list:
    j = i.split(" ")[3]  # GroupId 위치
    GroupId_list.append(j)

for GroupId in GroupId_list:
    try:
        response = ec2.delete_security_group(GroupId=GroupId)
        # response = ec2.delete_security_group(GroupName=GroupId+'HelloBOTO')
        print('Security Group Deleted')
        logger.info(GroupId+" Deleted")

    except ClientError as e:
        print(e)
        logger.error(e)
