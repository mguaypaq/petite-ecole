#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Code for working with Dyck paths.

A Dyck path is represented as a tuple, where each
entry gives the number of boxes above-and-to-the-right
of the baseline in a row.
"""

__all__ = [
    'all_dyck_paths',
    'is_dyck_path',
    'is_primitive',
    'boxes_under_path',
    ]

# ---------------------------------------------------------
import itertools as it
# ---------------------------------------------------------

#### insérer du code ici ####

# ---------------------------------------------------------
if __name__ == '__main__':
    import doctest
    doctest.testmod()
# ---------------------------------------------------------

