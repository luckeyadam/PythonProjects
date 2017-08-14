#!/usr/bin/env python
import boto3

"""
Security group operations
=========================
Creates security groups
"""


def create_sg(vpc_id, description, group_name):
    """
    Creates a security group to put new EC2 installations into
    :param vpc_id:
    :param description:
    :param group_name:
    :return:
    """
    client = boto3.client('ec2')
    security_group = str(group_name + "_sg")

    # get the security groups
    idle_sg = get_sg()

    print(idle_sg)
    print(security_group)

    # if security group doesnt exist, create it
    if security_group not in idle_sg:
        print("Creating SG")
        return client.create_security_group(
            Description=description,
            GroupName=security_group,
            VpcId=vpc_id
        )
    return get_sg_id(security_group)


def get_sg():
    """
    Returns a list of security groups that exist
    :return:
    """
    client = boto3.client('ec2')
    all_instances = client.describe_instances()
    all_sg = client.describe_security_groups()

    instance_sg_set = set()
    sg_set = set()

    for reservation in all_instances["Reservations"]:
        for instance in reservation["Instances"]:
            for sg in instance["SecurityGroups"]:
                instance_sg_set.add(sg["GroupName"])

    for security_group in all_sg["SecurityGroups"]:
        sg_set.add(security_group["GroupName"])

    idle_sg = sg_set - instance_sg_set

    return idle_sg


def get_sg_id(sg_name):
    """
    Return a security group id based on SG name
    (used when building EC2 instances since they require ID)
    :param sg_name:
    :return:
    """
    print()
    print("Searching for SG ID")
    client = boto3.client('ec2')
    all_sg = client.describe_security_groups()
    print(sg_name)
    grp_id = "None"
    for sec_grp in all_sg['SecurityGroups']:
        print(sec_grp['GroupName'])
        if sg_name == sec_grp['GroupName']:
            grp_id = sec_grp['GroupId']
    print()
    return grp_id
