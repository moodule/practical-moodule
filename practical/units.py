# -*- coding: utf-8 -*-

"""Unit conversion tools."""

import math

from practical.types import (
    typecheck,
    symbolic)

#####################################################################
# UNIT CONVERSION
#####################################################################

@typecheck
def convert_radian_to_degree(
        angle: symbolic) -> symbolic:
    """
    Unit conversion from radian to degree of angle.

    Parameters
    ----------
    angle:
        The angle measure, in radians.

    Returns
    -------
    out:
        The angle measure in degrees.
    """
    angle_in_degree = 180.0 * angle / math.pi
    return angle_in_degree

@typecheck
def convert_degree_to_radian(
        angle: symbolic) -> symbolic:
    """
    Unit conversion from degree to radian.

    Parameters
    ----------
    angle:
        The angle measure, in degrees.

    Returns
    -------
    out:
        The angle measure in radians.
    """
    angle_in_radian = math.pi * angle / 180.0
    return angle_in_radian
