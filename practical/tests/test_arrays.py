#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the type checking predicates."""

import numpy as np

import pytest
from numpy.testing import assert_allclose

import practical.arrays as arrays

#####################################################################
# DICT TO ARRAY CONVERSION
#####################################################################

def test_dict_to_array_conversion():
    data = {
        'dsf': 34,
        'olivier': sum([ord(c) for c in 'cgu']),
        'hell': 9.435}

    keys_1 = data.keys()    # iterable != list : should work too
    keys_2 = 2 * list(data.keys())
    keys_3 = list(data.keys()) + ['dummy_1', 'dummy_2'] + list(data.keys())

    array_1 = arrays.convert_dict_to_array(
        data=data,
        keys=keys_1,
        default=np.inf)

    array_2 = arrays.convert_dict_to_array(
        data=data,
        keys=keys_2)

    array_3 = arrays.convert_dict_to_array(
        data=data,
        keys=keys_3,
        default=-1.0)

    array_4 = arrays.convert_dict_to_array(
        data=data,
        keys=sorted(keys_3))

    array_5 = arrays.convert_dict_to_array(
        data=data)

    # test shapes
    assert array_1.shape == (1, 3)
    assert array_2.shape == (1, 6)
    assert array_3.shape == (1, 8)
    assert array_4.shape == (1, 8)
    assert array_5.shape == (1, 3)

    # test values
    for i, k in enumerate(data.keys()):
        assert array_1[0, i] == data[k]
        assert array_2[0, i] == data[k]
        assert array_2[0, i + len(data.keys())] == data[k]
        assert array_3[0, i] == data[k]
        assert array_3[0, i + 2 + len(data.keys())] == data[k]
        assert array_5[0, i] == data[k]

    assert array_3[0, keys_3.index('dummy_1')] == -1.0
    assert array_3[0, keys_3.index('dummy_2')] == -1.0

    for i, k in enumerate(sorted(keys_3)):
        assert array_4[0, i] == data.get(k, 0.0)
