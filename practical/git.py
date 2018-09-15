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
def add_files_to_github(
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
        _add_file(path)
    else:
        for p in path:
            _add_file(p)

@typecheck
def _add_file(
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
def commit_files_to_github(
        path: iterable=[],
        message: str='') -> None:
    """
    Commit the staged changes with git.

    Parameters
    ----------
    path:
        A string or list of strings representing absolute or relative path(s).

    Returns
    -------
    out: None.
    """
    commit_msg = message
    if not commit_msg:
        now = datetime.now()
        commit_msg = '"{}-{}-{}_{}-{}."'.format(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute)

    if path:
        add_files_to_github(path)

    sh.git.commit('-m', commit_msg)
