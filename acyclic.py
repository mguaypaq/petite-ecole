#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
Code for working with acyclic orientations on Dyck paths.

An orientation is represented as a triple `(n, ascents, descents)`
which partitions the boxes under the Dyck path (which must have
length `n`) into ascending and descending pairs, respectively.
"""

__all__ = [
    'all_orientations',
    'example',
    'graphical',
    'is_orientation',
    'single_sink',
    ]

# ---------------------------------------------------------

import itertools as it
from dyckpath import is_dyck_path, boxes_under_path

# ---------------------------------------------------------

def all_orientations(path):
    r"""
    Return all acyclic orientations of a Dyck path.

    >>> all(is_orientation(ao) for ao in all_orientations((1, 2, 1, 0)))
    True
    >>> len(list(all_orientations((1, 1, 1, 0))))
    8
    >>> len(list(all_orientations((3, 2, 1, 0))))
    24
    """
    n = len(path)
    result = set()
    for ordering in it.permutations(range(n)):
        ascents = set()
        descents = set()
        for (i, j) in boxes_under_path(path):
            if ordering[i] < ordering[j]:
                ascents.add((i, j))
            else:
                descents.add((i, j))
        ao = (n, frozenset(ascents), frozenset(descents))
        result.add(ao)
    return result

# ---------------------------------------------------------

def is_orientation(ao):
    r"""
    Check whether `ao` is a valid acyclic orientation.

    >>> from dyckpath import ascii
    >>> path = (1, 3, 2, 2, 1, 0)
    >>> print ascii(path)
         /\
        /\/\/\
     /\/\/\/\/\
    /\/\/\/\/\/\
    >>> all_boxes = frozenset(boxes_under_path(path))
    >>> ao = (len(path), all_boxes, frozenset())
    >>> is_orientation(ao)
    True
    >>> ao = (len(path), frozenset(), all_boxes)
    >>> is_orientation(ao)
    True
    >>> ascents = frozenset([
    ...     (1, 4),
    ...     (2, 3),
    ...     (2, 4),
    ...     (3, 4),
    ...     (3, 5),
    ...     (4, 5),
    ...     ])
    >>> descents = frozenset([
    ...     (0, 1),
    ...     (1, 2),
    ...     (1, 3),
    ...     ])
    >>> ao = (len(path), ascents, descents)
    >>> is_orientation(ao)
    True
    >>> not_ao = [len(path), ascents, descents]
    >>> is_orientation(not_ao)  # wrong type
    False
    >>> not_ao = (ascents, descents)
    >>> is_orientation(not_ao)  # wrong length
    False
    >>> not_ao = (ascents, descents, len(path))
    >>> is_orientation(not_ao)  # wrong order
    False
    >>> not_ao = (len(path), list(ascents), list(descents))
    >>> is_orientation(not_ao)  # wrong types
    False
    >>> not_ao = (len(path)-1, ascents, descents)
    >>> is_orientation(not_ao)  # wrong size
    False
    >>> not_ao = (len(path), ascents, frozenset())
    >>> is_orientation(not_ao)  # ascents and descents not exhaustive
    False
    >>> not_ao = (len(path), ascents, all_boxes)
    >>> is_orientation(not_ao)  # ascents and descents intersect
    False
    >>> not_ao = (3, frozenset([(0, 1), (1, 2)]), frozenset([(0, 2)]))
    >>> is_orientation(not_ao)  # cycle one way
    False
    >>> not_ao = (3, frozenset([(0, 2)]), frozenset([(0, 1), (1, 2)]))
    >>> is_orientation(not_ao)  # cycle the other way
    False
    """
    if not isinstance(ao, tuple): return False
    if not len(ao) == 3: return False
    n, ascents, descents = ao
    if not isinstance(n, int): return False
    if not isinstance(ascents, frozenset): return False
    if not isinstance(descents, frozenset): return False

    # compute the underlying Dyck path
    path = [0]*n
    try:
        for (i, j) in ascents: path[i] += 1
        for (i, j) in descents: path[i] += 1
    except (ValueError, TypeError, IndexError):
        return False
    path = tuple(path)

    if not is_dyck_path(path): return False
    if not ascents.isdisjoint(descents): return False
    if not ascents.union(descents) == boxes_under_path(path): return False

    # check for 3-cycles
    for i, j, k in it.combinations(range(n), 3):
        if ((i, j) in ascents and
            (j, k) in ascents and
            (i, k) in descents):
            return False
        if ((i, j) in descents and
            (j, k) in descents and
            (i, k) in ascents):
            return False
    return True

def example():
    r"""
    Return an example of a valid acyclic orientation.

    >>> ao = example()
    >>> is_orientation(ao)
    True
    """
    ascents = frozenset([
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
        (3, 5),
        (4, 5),
        ])
    descents = frozenset([
        (0, 1),
        (1, 2),
        (1, 3),
        ])
    ao = (6, ascents, descents)
    return ao

def graphical(ao):
    r"""
    Return a sage graphics representation of the given acyclic orientation.
    """
    from sage.all import Graphics, point, line
    assert is_orientation(ao)
    n, ascents, descents = ao

    # compute heights
    height = [0]*n
    for _ in range(n):
        for (i, j) in ascents:
            height[j] = max(height[j], height[i]+1)
        for (i, j) in descents:
            height[i] = max(height[i], height[j]+1)

    # compute the extent of each interval
    left = range(n)
    right = range(n)
    for (i, j) in ascents:
        right[i] += .75
        left[j] -= .75
    for (i, j) in descents:
        right[i] += .75
        left[j] -= .75

    result = Graphics()

    # put in the ascents and descents
    for (i, j) in ascents:
        result += line([(i, height[i]), (j, height[j])],
                       color='red', thickness=2)
    for (i, j) in descents:
        result += line([(i, height[i]), (j, height[j])],
                       color='blue', thickness=2)

    # then put in the intervals
    for i in range(n):
        result += line([(left[i], height[i]), (right[i], height[i])],
                       color='black', thickness=2)
        result += point([(i, height[i])],
                       color='black', size=100)

    # reset some annoying options
    result.axes(False)
    result.set_aspect_ratio(1)
    return result

# ---------------------------------------------------------
if __name__ == '__main__':
    import doctest
    doctest.testmod()
# ---------------------------------------------------------

