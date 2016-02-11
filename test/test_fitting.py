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

from unittest import TestCase

from eao_util import fitting


class FittingTest(TestCase):
    def test_pre_bin_data(self):
        data = [
            [4,  150, 90],
            [5,  160, 91],
            [6,  200, 92],
            [15, 180, 93],
        ]

        columns = [10, True, False]

        result = fitting.pre_bin_data(data, columns, n_min=3)

        self.assertEqual(result, [[5, 160]])

        result = fitting.pre_bin_data(data, columns, method='mean', n_min=1)

        self.assertEqual(sorted(result), [[5, 170], [15, 180]])
