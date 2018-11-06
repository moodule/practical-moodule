# -*- coding: utf-8 -*-

"""
============
Web scraping
============

Utilities to extract meaningful information from the web.

Examples
--------
    >>> 
"""

from __future__ import division, print_function, absolute_import

from bs4 import BeautifulSoup

from practical.types import typecheck

#####################################################################
# TEXT EXTRACTION
#####################################################################

@typecheck
def extract_text_from_html_markup(
        html:str) -> str:
    """
    Extract the text *visible* to a user on an internet browser,
    from a string of html markup.

    The chunks of text are separated by newlines.

    Parameters
    ----------
    html: str.
        A string of html markup soup.

    Returns
    -------
    out: str.
        The visible text.
    """
    soup = BeautifulSoup(markup=html, features="lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("."))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
