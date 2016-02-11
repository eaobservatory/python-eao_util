# Copyright (C) 2016 East Asian Observatory
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

from collections import defaultdict

import numpy as np


def pre_bin_data(data, columns, method='median', n_min=10):
    """
    Take raw data (to be used for fitting) and pre-bin it.

    The idea is to derive an average value for each bin and use those
    to do the subsequent analysis.  Each value represents our best
    knowledge of the behavior of the system in a particular region of
    the parameter space.  Often our sampling of the space is very
    uneven, causing the fitting process to be swamped with values
    from the high density areas such that it gives little weight to
    other areas and thus derives a poor fit there.

    `data` should be a list of measurements (the rows), each with a
    number of values (the columns).  The columns should correspond to
    the list given via the `columns` argument.  This list should contain
    the width of the bins to use for that column, `True` if this is a
    measured value (to be averaged in the bins) or `False` to ignore the
    column.  The dimensionality of the bins will be the number of elements
    in the `columns` list which specify widths.
    """

    # Determine number of non-ignored columns and create a "defaultdict"
    # to contain lists of that many lists.
    n_col = 0
    for column in columns:
        if column is not False:
            n_col += 1

    if not n_col:
        raise Exception('No non-ignored columns specified')

    def make_lists():
        lists = []
        for i in range(0, n_col):
            lists.append(list())
        return lists

    binned = defaultdict(make_lists)

    # Go through the input data and accumulate the non-ignored columns in
    # bins.
    for row in data:
        row_key = []
        row_value = []

        for (column, value) in zip(columns, row):
            if column is False:
                continue

            row_value.append(value)

            if column is not True:
                row_key.append(int(value / column))

        for (bin_, value) in zip(binned[tuple(row_key)], row_value):
            bin_.append(value)

    # For each bin, calculate the average.
    results = []

    for bin_ in binned.values():
        if len(bin_[0]) < n_min:
            continue

        result = []

        for values in bin_:
            if method == 'median':
                result.append(np.median(values))

            elif method == 'mean':
                result.append(np.mean(values))

            else:
                raise Exception('Unknown binning method "{}"'.format(method))

        results.append(result)

    return results
