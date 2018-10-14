# -*- coding: utf-8 -*-

"""
================
Type enforcement
================

Function decorators to check function arguments and return values against
specified types or predicates.

Examples
--------
    >>> @typecheck
    ... def average(x: int, y:int, z:int) -> float:
    ...     return (x + y + z) / 2
    ...
    >>> average(5.5, 10, 15.0)
    TypeWarning:  'average' method accepts (int, int, int), but was given
    (float, int, float)
    15.25
    >>> average(5, 10, 15)
    TypeWarning:  'average' method returns (float), but result is (int)
    15
"""

from __future__ import division, print_function, absolute_import

from decorator import decorator
import inspect
import numpy as np
import sympy as smp

#####################################################################
# MESSAGES
#####################################################################

def function_arg_types_error(
        fname: str,
        expected: str,
        actual: str,
        flag: int) -> str:
    """
    Convenience function returns nicely formatted error/warning msg.

    Parameters
    ----------
    fname: str.
        The name of the function that failed.
    expected: type list.
        The expected type for each parameter.
    actual: type list.
        The types of the given arguments.
    flag: int.
        Whether it was the input or the output that didn't match.

    Returns
    -------
    out: str.
        The error/warning message.
    """
    return "'{}' ".format(fname)\
          + ("accepts ({}), but ", "returns {}, but ")[flag].format(expected)\
          + ("was given", "result is")[flag] + " {}".format(actual)

#####################################################################
# TYPE ENFORCEMENT
#####################################################################

def _check(arg, checker):
    """
    Check a given argument against either a type or a predicate.

    Parameters
    ----------
    arg: anything.
        The argument value.
    checker: type or callable.
        A callable giving a boolean value for any value.

    Returns
    -------
    out: bool.
        Whether the argument satisfies the input constraints.
    """
    if type(checker) == type:
        return isinstance(arg, checker)     #types
    elif callable(checker):
        return checker(arg)                 #predicates
    else:
        return True   

@decorator
def typecheck(func, *args):
    """
    Function decorator. Checks decorated function is given valid arguments,
    following the information written in the annotations.

    Parameters
    ----------
    func: callable.
        A function on which we want to enforce type checking.

    Returns
    -------
    out: callable.
        The decorated function.
    """
    result = func(*args)

    if hasattr(func, '__annotations__') and func.__annotations__:
        arg_spec = inspect.getfullargspec(func)

        for argname, arg in zip(arg_spec.args, args):
            if argname in func.__annotations__:
                checker = func.__annotations__[argname]
                if not _check(arg, checker):
                    msg = function_arg_types_error(
                        func.__name__,
                        "{}:{}".format(argname, checker),
                        "{}={}".format(argname, repr(type(arg))),
                        0)
                    raise TypeError(msg)

        if 'return' in func.__annotations__:
            checker = func.__annotations__['return']
            if not _check(result, checker):
                msg = function_arg_types_error(
                    func.__name__,
                    "{}".format(checker),
                    repr(type(result)),
                    1)
                raise TypeError(msg)

    return result

#####################################################################
# GENERIC PREDICATES
#####################################################################

@typecheck
def anything(x) -> bool:
    """
    Accepts all the input values.

    Parameters
    ----------
    x :
        An argument to check.

    Returns
    -------
    out: bool.
        Always True.
    """
    return True

@typecheck
def nothing(x) -> bool:
    """
    Checks whether an input is None.

    Parameters
    ----------
    x :
        An argument to check.

    Returns
    -------
    out: bool.
        True if x is None.
    """
    return x is None

@typecheck
def one_of(*checkers) -> callable:
    """
    Checks whether an input satisfies at least one of the given checkers.

    Parameters
    ----------
    checkers: list.
        List of checker callables.

    Returns
    -------
    out: bool.
        True of any of the checkers is satisfied.
    """
    def _one_of(x):
        return any([
            checker(x)
            for checker in checkers])

    return _one_of

@typecheck
def iterable(x) -> bool:
    """
    Checks whether an object is iterable.

    Parameters
    ----------
    x:
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is iterable.
    """
    try:
        it = iter(x)
    except TypeError:
        return False
    else:
        return True

#####################################################################
# NUMERIC PREDICATES
#####################################################################

@typecheck
def numeric(x) -> bool:
    """
    Checks a value against all the numeric types at once :
    int, float, np.float64...

    Parameters
    ----------
    x:
        An argument to check.

    Returns
    -------
    out: bool.
    """
    try:
        float(x)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True

@typecheck
def finite(x) -> bool:
    """
    Checks whether the input is a finite numeric value.

    Parameters
    ----------
    x:
        An argument to check.

    Returns
    -------
    out: bool.
        True when the argument is finite.
    """
    try:
        bool(np.all(np.isfinite(x)))
    except TypeError:
        return False
    else:
        if iterable(x):
            return False
        else:
            return bool(np.isfinite(x))

#####################################################################
# SYMBOLIC PREDICATES
#####################################################################

@typecheck
def symbolic(x) -> bool:
    """
    Checks whether the input is a symbolic expression ; any class
    derived from sympy core qualify.

    Parameters
    ----------
    x:
        An argument to check.

    Returns
    -------
    out: bool.
        True if the argument is a symbolic expression.
    """
    return numeric(x) or isinstance(x, smp.Expr)

#####################################################################
# BOUNDS PREDICATES
#####################################################################

@typecheck
def _check_bounds_tuple(x) -> bool:
    """
    Checks whether a tuple is a valid bound.

    Parameters
    ----------
    x: a tuple.
        Represents the lower and upper bounds.

    Returns
    -------
    out: bool.
        True if the argument is a valid bound tuple.
    """
    is_valid = (
        bool(x) and
        isinstance(x, tuple) and
        len(x) == 2 and
        numeric(x[0]) and
        numeric(x[1]) and
        bool(x[0] <= x[1])) # cast from np.bool_ !!

    return is_valid

@typecheck
def _check_bounds_dict(x) -> bool:
    """
    Checks whether a dict represents valid bounds.

    Parameters
    ----------
    x: dict.
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is valid bounds.
    """
    is_valid = (
        bool(x)
        and isinstance(x, dict)
        and all(map(
            lambda t: _check_bounds_tuple(x=t),
            x.values())))
    
    return is_valid

@typecheck
def _check_bounds_array(x) -> bool:
    """
    Checks whether a np.ndarray represents valid bounds.

    Parameters
    ----------
    x: np.ndarray.
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is valid bounds.
    """
    is_valid = (
        isinstance(x, np.ndarray)
        and len(x.shape) == 2
        and x.shape[1] == 2
        and all(map(
            lambda t: _check_bounds_tuple(x=t),
            [tuple(line) for line in x])))

    return is_valid

@typecheck
def bounds(x) -> bool:
    """
    Checks whether an argument represents valid bounds.

    Parameters
    ----------
    x:
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is valid bounds.
    """
    if isinstance(x, tuple):
        return _check_bounds_tuple(x)
    elif isinstance(x, dict):
        return _check_bounds_dict(x)
    elif isinstance(x, np.ndarray):
        return _check_bounds_array(x)
    else:
        return False

#####################################################################
# SPECIFICATIONS PREDICATES
#####################################################################

@typecheck
def specifications(x) -> bool:
    """
    Checks whether an argument represents valid specifications.

    Parameters
    ----------
    x:
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is valid specifications.
    """
    return (
        isinstance(x, dict)
        and bounds(x)
        and all([finite(v[0]) for k, v in x.items()])
        and all([finite(v[1]) for k, v in x.items()]))

#####################################################################
# TRACE & CHARTS PREDICATES
#####################################################################

@typecheck
def trace_data(x) -> bool:
    """
    Checks whether an argument contains graphing data.

    Parameters
    ----------
    x:
        The argument to check.

    Returns
    -------
    out: bool.
        True if the argument is valid data for a trace.
    """
    return (
        isinstance(x, dict)
        and (
            'x' in x.keys()
            and iterable(x.get('x'))
            and bool(x.get('x'))
            and all(map(finite, x.get('x'))))
        and (
            'y' in x.keys()
            and iterable(x.get('y'))
            and bool(x.get('y'))
            and all(map(finite, x.get('y'))))
        and len(x.get('x')) == len(x.get('y'))
        and 'name' in x.keys())

#####################################################################
# MATRIX & ARRAY PREDICATES
#####################################################################
