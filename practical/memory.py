# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

from decorator import decorator

#####################################################################
# MEMOIZATION
#####################################################################

@decorator
def memoize(func, *args, **kwargs):
    if not hasattr(func, '__cache__'):
        setattr(func, '__cache__', dict())

    key = str(args) + str(kwargs)
    if key not in func.__cache__:
        func.__cache__[key] = func(*args, **kwargs)
    
    return func.__cache__[key]