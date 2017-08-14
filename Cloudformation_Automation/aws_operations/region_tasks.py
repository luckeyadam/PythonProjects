#!/usr/bin/env python
import boto3

"""
List the regions/AZ's
============================
Uses boto3 ec2 module to get Regions list
"""


def get_regions():
    """
    return a list of regions
    :return:
    """
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions
