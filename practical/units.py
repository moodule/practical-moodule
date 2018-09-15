# -*- coding: utf-8 -*-

import math

"""Unit conversion tools."""

#####################################################################
# UNIT CONVERSION
#####################################################################

def convert_radian_to_degree(angle):
    """
    Unit conversion from radian to degree of angle.

    Args:
        angle: the angle measure, in radians.

    Returns:
        the angle measure in degrees.
    """
    angle_in_degree = 180.0 * angle / math.pi
    return angle_in_degree

def convert_degree_to_radian(angle):
    """
    Unit conversion from degree to radian.

    Args:
        angle: the angle measure, in degrees.

    Returns:
        the angle measure in radians.
    """
    angle_in_radian = math.pi * angle / 180.0
    return angle_in_radian
