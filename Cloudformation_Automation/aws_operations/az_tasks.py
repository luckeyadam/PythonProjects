#!/usr/bin/env python
import boto3

"""
Get Availability Zone details
=========================
Uses ec2 module of boto3 to connect to availability zones
This is unused at the moment, but leaving it in for future use
"""


def get_az():
    """
    print the AZ's
    :return:
    """
    ec2 = boto3.client('ec2')
    # Retrieves all regions/endpoints that work with EC2 (leaving this here for future use maybe)
    # response = ec2.describe_regions()
    # print('Regions:', response['Regions'])

    # Retrieves availability zones only for region of the ec2 object
    response = ec2.describe_availability_zones()
    for zone in response['AvailabilityZones']:
        print(zone['ZoneName'])
