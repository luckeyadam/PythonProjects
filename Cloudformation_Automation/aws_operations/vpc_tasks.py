#!/usr/bin/env python
import boto3

"""
Get VPC details by region
=========================
Uses ec2 module of boto3 to connect to aws region
- parses list of vpcs and if the vpc has a name, adds it to a dict with the vpc id
"""


def get_vpc():
    '''
    connect to ec2 region and get vpc details, returns dict of vpc and name values
    :param region:
    :return:
    '''
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')
    filters = [{'Name': 'tag:Name', 'Values': ['*']}]
    vpcs = []
    try:
        vpcs = list(ec2.vpcs.filter(Filters=filters))
    except KeyError:
        print("No VPCs found")

    vpcdict = []

    # for each VPC if it has a name, put the name and vpc id in a dictionary for later use
    for vpc in vpcs:
        response = client.describe_vpcs(
            VpcIds=[
                vpc.id,
            ]
        )
        for eachvpc in response['Vpcs']:
            for taglist in eachvpc['Tags']:
                if 'Name' in taglist['Key']:
                    vpcdict.append(taglist['Value']+" "+eachvpc['VpcId'])
                else:
                    vpcdict.append(taglist['Value'] + " " + eachvpc['VpcId'])

    print(vpcdict)
    return vpcdict

# return the subnet id
def return_vpc_id(vpc_name):
    """
    return only the id from the vpc name generated in the get_vpc function
    :param subnet_name:
    :return:
    """
    return (vpc_name.rsplit(None, 1)[-1])
