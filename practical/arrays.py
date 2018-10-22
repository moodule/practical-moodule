# -*- coding: utf-8 -*-

"""
==========================
Matrices & vector handling
==========================

"""

from __future__ import division, print_function, absolute_import

from decorator import decorator
import numpy as np

from practical.types import (
    anything,
    iterable,
    nothing,
    numeric,
    one_of,
    typecheck)

#####################################################################
# SHAPE ENFORCING
#####################################################################

@typecheck
def _reshape(
        arg: anything,
        shape: tuple) -> anything:
    """
    Reshapes any object.
    Checks whether the object is an array and the shape is valid.

    Parameters
    ----------
    x:
        Anything.
    shape: tuple.
        A tuple of integers ; can ba empty.

    Returns
    -------
    out:
        Anything, but reshaped if the conditions are met.
    """
    if shape and isinstance(arg, np.ndarray):
        return np.reshape(
            a=arg,
            newshape=shape)
    else:
        return arg

@typecheck
def reshapes(
        *shapes) -> callable:
    """
    Function decorator. Check whether the ndarray arguments match the
    required shapes.

    Parameters
    ----------
    shapes: list of tuples.
        The expected shapes for each ndarray argument.
        For non array types, provide an empty tuple.

    Returns
    -------
    out: caller function, decorated.
        All the ndarray arguments are reshaped.
    """
    def caller(f, *args, **kwargs):
        assert (
            len(args) == len(shapes)
            or len(args) + 1 == len(shapes))

        reshaped_args = [
            _reshape(arg=arg, shape=shapes[i])
            for i, arg in enumerate(args)]

        if len(shapes) == len(args) + 1:     # shape the return value
            return _reshape(
                arg=f(*reshaped_args, **kwargs),
                shape=shapes[-1])
        else:
            return f(*reshaped_args, **kwargs)

    return decorator(caller)

#####################################################################
# LINEAR ALGEBRA & ARRAY MANIPULATIONS
#####################################################################

@typecheck
def convert_dict_to_array(
        data: dict,
        keys: one_of(nothing, iterable) = None,
        default: numeric = 0.0) -> np.ndarray:
    """
    Creates an array with the size of keys, filling missing dimensions.

    Parameters
    ----------
    data: dict.
        The dictionary to convert.
    keys: list of string
        The FULL list of axes keys.

    Returns
    -------
    out: np.array.
        The array, with the size of keys.
    """
    axes = keys if keys else data.keys()

    data_list = [
        data.get(a, default) 
        for a in axes]

    data_array = np.array(data_list)

    return data_array

@typecheck
def reshape_into_matrix(
        data: np.ndarray,
        shape: tuple) -> np.ndarray:
    """
    Parameters
    ----------

    Returns
    -------
    """
    return np.reshape(
        a=data,
        newshape=shape,
        order='C')

@typecheck
def reshape_into_vector(
        data: np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------

    Returns
    -------
    """
    return np.reshape(
        a=data,
        newshape=(-1,),
        order='C')
