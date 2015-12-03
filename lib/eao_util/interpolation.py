# Copyright (C) 2015 East Asian Observatory
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful,but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

from __future__ import absolute_import, division, print_function, \
    unicode_literals


def compress_list(values, tolerance=0.001):
    """
    Reduce the number of points in a list to be used for linear interpolation.

    Given a list of (x, y) pairs, remove "unnecessary" points and return
    the trimmed list of pairs.  Points are removed if, without them, a linear
    interpolation between enclosing remaining points would recover the
    input values within the given (absolute) tolerance.

    This function is very slow, but since it is used infrequently to generate
    the lookup tables used by other programs, this is not too problematic.
    """

    # Make copy of list for modification.
    trimmed = list(values)

    while True:
        # Counter of how many points we removed this iteration.
        n = 0

        for i in range(len(trimmed) - 2, 0, -1):
            (before_f, before_d) = trimmed[i - 1]
            (after_f, after_d) = trimmed[i + 1]

            for (value_f, value_d) in values:
                if not (before_f < value_f < after_f):
                    continue

                interp = (
                    before_d +
                    ((after_d - before_d) *
                     (value_f - before_f) /
                     (after_f - before_f)))

                if abs(interp - value_d) > tolerance:
                    break

            else:
                del trimmed[i]
                n += 1

        # Stop if we didn't find any points to remove.
        if not n:
            break

    return trimmed
