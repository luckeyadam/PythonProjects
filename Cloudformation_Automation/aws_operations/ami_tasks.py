#!/usr/bin/env python
import boto3

"""
Get AMI details
=========================
Uses ec2 module of boto3 to connect to availability zones
"""


def get_amis():
    """
    get a list of all AMIs accessible by the account user
    :return:
    """
    client = boto3.client('ec2')
    id = boto3.client('sts').get_caller_identity().get('Account')
    filters = [{'Name': 'owner-id', 'Values': [id]}]
    images = client.describe_images(Filters=filters)
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return parse_imageid_name(images)


def parse_imageid_name(images):
    """
    Returns a list of AMIs including tag name descriptions if available
    :param images:
    :return:
    """
    print(images)
    image_list = []
    for image in images['Images']:
        image_list.append(image['Name'] + " " + image['ImageId'])
    return image_list


def return_image_id(image_name):
    """
    Return the image name as parsed from the string created in the parse_imageid_name function
    :param image_name:
    :return:
    """
    return (image_name.rsplit(None, 1)[-1])
