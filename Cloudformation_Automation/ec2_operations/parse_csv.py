#!/usr/bin/env python
import csv

"""
Open a csv and return list of items from csv
"""
# currently unused in the applicaiton
def open_file(filename):
    """
    Returns a list from a csv
    :param filename:
    :return: a list
    """
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        host_list = list(reader)
    return host_list[0]