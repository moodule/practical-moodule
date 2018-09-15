#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests the type checking predicates."""

import numpy as np

import pytest
from numpy.testing import assert_allclose
from timeit import timeit

from practical.memory import memoize

#####################################################################
# MEMOIZATION
#####################################################################
def f1_raw():
    with open('./README.rst', 'r') as file:
        result = [line.upper() for line in file]
    return "\n".join(result)

@memoize
def f1_mem():
    with open('./README.rst', 'r') as file:
        result = [line.upper() for line in file]
    return "\n".join(result)

def test_memoize_performance():
    raw_t = timeit("f1_raw()", number=10000, globals=globals())

    mem_t = timeit("f1_mem()", number=10000, globals=globals())

    assert mem_t < 0.1 * raw_t

    print(mem_t, raw_t)

def memoize_identity():
    assert f1_raw() == f1_mem()
