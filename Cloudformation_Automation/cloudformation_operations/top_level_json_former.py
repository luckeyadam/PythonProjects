#!/usr/bin/env python
"""
Forms top level json for the cloudformation template
====================================================
"""


def get_formation_telmplate():
    """
    return the base cloudformation template
    :return:
    """
    output_json = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {}
    }
    return output_json
