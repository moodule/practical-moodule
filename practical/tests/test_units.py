#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the unit conversions."""

import math

import pytest
from numpy.testing import assert_allclose

import practical.units as units

#####################################################################
# ANGLE CONVERSIONS
#####################################################################

def test_radian_to_degree_conversion():
    assert units.convert_radian_to_degree(0.0) == 0.0
    assert_allclose(units.convert_radian_to_degree(math.pi), 180.0, rtol=1e-6)
    assert_allclose(units.convert_radian_to_degree(-0.5 * math.pi), -90.0, rtol=1e-6)

def test_degree_to_radian_conversion():
    assert units.convert_degree_to_radian(0.0) == 0.0
    assert_allclose(units.convert_degree_to_radian(180.0), math.pi, rtol=1e-6)
    assert_allclose(units.convert_degree_to_radian(-45.0), -0.25 * math.pi, rtol=1e-6)

def test_identity():
    assert_allclose(
        units.convert_radian_to_degree(
            units.convert_degree_to_radian(180.0)),
        180.0,
        rtol=1e-6)

    assert_allclose(
        units.convert_degree_to_radian(
            units.convert_radian_to_degree(0.25 * math.pi)),
        0.25 * math.pi,
        rtol=1e-6)

    assert_allclose(
        units.convert_radian_to_degree(
            units.convert_degree_to_radian(9845.3057)),
        9845.3057,
        rtol=1e-6)
