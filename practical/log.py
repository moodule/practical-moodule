# -*- coding: utf-8 -*-

"""
======================
Console & file logging
======================

Examples
--------
    >>> 
"""

from __future__ import division, print_function, absolute_import

import sys

from practical.types import *

#####################################################################
# MESSAGES
#####################################################################

@typecheck
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

@typecheck
def function_arg_count_error(
        fname: str,
        expected: int,
        actual: int) -> str:
    """
    Generates an error/warning message when a function is called with
    an invalid number of argument.

    Parameters
    ----------
    fname: str.
        The name of the function that failed.
    expected: int.
        The expected number of arguments.
    actual: int.
        The given number of arguments.

    Returns
    -------
    out: str.
        The error/warning message.
    """
    return "{}() takes exactly {} positional argument ({} given)".format(
        fname,
        expected,
        actual)

#####################################################################
# LOG
#####################################################################

@typecheck
def console_log(
        msg: str,
        lvl: int=1) -> None:
    """
    Directs the msg to the stream corresponding to the given level of
    debugging.

    Parameters
    ----------
    msg: str.
    lvl: int.

    Returns
    -------
    out: None.
    """
    if lvl is 1:
        print('TypeWarning: ', msg, file=sys.stderr)
    elif lvl is 2:
        raise TypeError(msg)
