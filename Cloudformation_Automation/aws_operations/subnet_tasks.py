#!/usr/bin/env python
import boto3

"""
Get Subnet details by VPC
=========================
Uses ec2 module of boto3 to connect to VPCs
- lists all vpcs, then for each vpc and each az in that vpc, lists subnets
"""


def get_subnets():
    '''
    connect to ec2 region and get subnet details, returns dict of subnet and name values
    The names returned have the tags and AZ prepended if the exist
    :param region:
    :return:
    '''
    ec2 = boto3.resource("ec2")
    vpcs = list(ec2.vpcs.all())
    return_subnets = []
    for vpc in vpcs:
        for az in ec2.meta.client.describe_availability_zones()["AvailabilityZones"]:
            for subnet in vpc.subnets.filter(Filters=[{"Name": "availabilityZone", "Values": [az["ZoneName"]]}]):
                tags = "NoTagsSet"
                if vpc.tags != None:
                    tags = vpc.tags[0]['Value']
                return_subnets.append(str(tags + " " + az["ZoneName"] + " " + subnet.id))

    return return_subnets


# return the subnet id
def return_subnet_id(subnet_name):
    """
    return only the id from the subnet name generated in the get_subnets function
    :param subnet_name:
    :return:
    """
    return (subnet_name.rsplit(None, 1)[-1])
