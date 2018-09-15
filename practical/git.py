# -*- coding: utf-8 -*-

"""
=============
GIT UTILITIES
=============


"""

from __future__ import division, print_function, absolute_import

from datetime import datetime
import os
import sh

from practical.types import *

#####################################################################
# ADD
#####################################################################

@typecheck
def stage_files(
        path: iterable) -> None:
    """
    Stage files with git.

    Parameters
    ----------
    path:
        A string or list of strings representing absolute or relative path(s).

    Returns
    -------
    out: None.
    """
    if isinstance(path, str):
        _stage_file(path)
    else:
        for p in path:
            _stage_file(p)

@typecheck
def _stage_file(
        path: one_of(os.path.isdir, os.path.isfile)) -> None:
    """
    Utility function to stage a single file with git.
    Checks the validity of the given path.

    Parameters
    ----------
    path: str.
        A string representing the absolute or relative path to a file.

    Returns
    -------
    out: None.
    """
    sh.git.add(path)

#####################################################################
# COMMIT
#####################################################################

@typecheck
def commit_to_github(
        message: str) -> None:
    """
    Commit the staged changes with git.

    Parameters
    ----------
    message: str.
        The description of the staged changes.

    Returns
    -------
    out: None.
    """
    sh.git.commit('-m', message)
