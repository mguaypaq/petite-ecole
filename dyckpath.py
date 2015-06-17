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
    'ascii',
    'boxes_under_path',
    'graphical',
    'is_dyck_path',
    'is_primitive',
    ]

# ---------------------------------------------------------

import itertools as it

# ---------------------------------------------------------

def is_dyck_path(path):
    r"""
    Check whether `path` is a valid Dyck path.

    The entries of `path` give the number of boxes
    above the path in each row.

    >>> is_dyck_path((0, 0, 0))
    True
    >>> is_dyck_path((1, 0, 0))
    True
    >>> is_dyck_path((0, 1, 0))
    True
    >>> is_dyck_path((1, 1, 0))
    True
    >>> is_dyck_path((2, 1, 0))
    True
    >>> is_dyck_path((1, 2, 0))
    False
    """
    return (isinstance(path, tuple) and
            all(isinstance(entry, int) for entry in path) and
            all(entry >= 0 for entry in path) and
            all(path[i] < path[i+1]+2 for i in range(len(path)-1)) and
            (len(path) == 0 or path[-1] == 0))

def is_primitive(path):
    r"""
    Check whether the Dyck path `path` is a primitive.

    >>> is_primitive((0, 0, 0))
    False
    >>> is_primitive((1, 0, 0))
    False
    >>> is_primitive((0, 1, 0))
    False
    >>> is_primitive((1, 1, 0))
    True
    >>> is_primitive((2, 1, 0))
    True
    """
    return (len(path) == 0 or path.index(0) == len(path)-1)

def all_dyck_paths(n, primitive=False):
    r"""
    An iterator over all valid Dyck paths of length `n`.

    If the optional keywork `primitive` is `True`, the iterator
    only generates paths that don't touch the baseline partway
    through the path.

    >>> for path in sorted(all_dyck_paths(3)): print path
    (0, 0, 0)
    (0, 1, 0)
    (1, 0, 0)
    (1, 1, 0)
    (2, 1, 0)
    >>> for path in sorted(all_dyck_paths(3, primitive=True)): print path
    (1, 1, 0)
    (2, 1, 0)
    >>> [len(list(all_dyck_paths(n))) for n in range(7)]
    [1, 1, 2, 5, 14, 42, 132]
    >>> [len(list(all_dyck_paths(n, primitive=True))) for n in range(7)]
    [1, 1, 1, 2, 5, 14, 42]
    """
    if n == 0:
        yield ()
        return
    elif n == 1:
        yield (0,)
        return
    elif n >= 2:
        for tail in all_dyck_paths(n-1, primitive=primitive):
            for head in range(primitive, tail[0]+2):
                yield (head,) + tail
        return

_cache = {}
def boxes_under_path(path):
    r"""
    Version mémoisée de _boxes_under_path.
    """
    if path in _cache:
        return _cache[path]
    else:
        result = _boxes_under_path(path)
        _cache[path] = result
        return result

def _boxes_under_path(path):
    r"""
    Return the set of boxes `(i, j)` below the path `path`.

    >>> sorted(boxes_under_path((0, 0, 0)))
    []
    >>> sorted(boxes_under_path((1, 0, 0)))
    [(0, 1)]
    >>> sorted(boxes_under_path((0, 1, 0)))
    [(1, 2)]
    >>> sorted(boxes_under_path((1, 1, 0)))
    [(0, 1), (1, 2)]
    >>> sorted(boxes_under_path((2, 1, 0)))
    [(0, 1), (0, 2), (1, 2)]
    >>> all(len(boxes_under_path(p)) == sum(p) for p in all_dyck_paths(5))
    True
    """
    return {(i, j) for i, k in enumerate(path) for j in range(i+1, i+1+k)}

# ---------------------------------------------------------

def ascii(path):
    r"""
    Return an ascii art representation of `path`.

    >>> print ascii((0, 0, 0))
    /\/\/\
    >>> print ascii((1, 0, 0))
     /\
    /\/\/\
    >>> print ascii((0, 1, 0))
       /\
    /\/\/\
    >>> print ascii((1, 1, 0))
     /\/\
    /\/\/\
    >>> print ascii((2, 1, 0))
      /\
     /\/\
    /\/\/\
    """
    assert is_dyck_path(path)
    rows = []
    for height in range(max(path)+1):
        row = ' '*height
        for entry in path:
            row += '/\\' if entry >= height else '  '
        rows.append(row.rstrip())
    return '\n'.join(reversed(rows))

def graphical(path):
    r"""
    Return a sage graphics representation of `path`.
    """
    from sage.all import Graphics, polygon
    assert is_dyck_path(path)
    result = Graphics()
    # first a row of triangles
    for i in range(len(path)):
        result += polygon([(2*i, 0),
                           (2*i+1, 1),
                           (2*i+2, 0)],
                          color='black', fill=False, thickness=2)
    # then all the boxes
    for i, j in boxes_under_path(path):
        result += polygon([(i+j, j-i),
                           (i+j+1, j-i+1),
                           (i+j+2, j-i),
                           (i+j+1, j-i-1)],
                          color='black', fill=False, thickness=2)
    # reset some annoying options
    result.axes(False)
    result.set_aspect_ratio(1)
    return result

# ---------------------------------------------------------

def test_generation(max_n=6):
    r"""
    Test that `all_dyck_paths` corresponds to `is_dyck_path`
    and `is_primitive`.

    >>> test_generation()
    """
    for n in range(max_n+1):
        iterated = sorted(all_dyck_paths(n))
        filtered = filter(is_dyck_path, it.product(range(n), repeat=n))
        assert iterated == filtered
        primitive_iterated = sorted(all_dyck_paths(n, primitive=True))
        primitive_filtered = filter(is_primitive, filtered)
        assert primitive_iterated == primitive_filtered

# ---------------------------------------------------------
if __name__ == '__main__':
    import doctest
    doctest.testmod()
# ---------------------------------------------------------

