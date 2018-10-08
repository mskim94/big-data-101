import boto3
import time
import logging
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

response = ec2.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

logger = logging.getLogger('vpc')
hdlr = logging.FileHandler('new_vpc.log')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger.addHandler(hdlr)
hdlr.setFormatter(formatter)
logger.setLevel(logging.INFO)

for i in range(10):
    try:
        response = ec2.create_security_group(GroupName=str(i)+'HelloBOTO',
                                             Description='Made by boto3',
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
        logger.info(security_group_id+" Added")

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
        # time.sleep(5)

    except ClientError as e:
        print(e)
        logger.error(e)
