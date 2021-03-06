#!/usr/bin/env python
from security_group_operations import sg_operations

"""
Open a csv and return list of items from csv
"""


def build_webapp(ec2_type, installation_name, webapp_number, top_level_json, az, subnet, ami):
    """
    Builds cloudformation template for an ec2 instance
    :param ec2_type:
    :param installation_name:
    :param webapp_number:
    :param top_level_json:
    :param az:
    :param subnet:
    :param ami:
    :return:
    """
    webapp_name = installation_name + webapp_number
    sg = sg_operations.get_sg_id(installation_name)
    top_level_json["Resources"][webapp_name] = {"Type": "AWS::EC2::Instance",
                                                "Properties": {
                                                    "InstanceType": ec2_type,
                                                    "ImageId": ami,
                                                    "Monitoring": "true",
                                                    "Tags": [
                                                        {"Key": "Name", "Value": webapp_name}
                                                    ],

                                                    "NetworkInterfaces": [
                                                        {
                                                            "DeleteOnTermination": "true",
                                                            "Description": "Primary network interface",
                                                            "DeviceIndex": 0,
                                                            "SubnetId": subnet,
                                                            "GroupSet": [str(sg)]
                                                        }
                                                    ]
                                                }}

    return top_level_json
