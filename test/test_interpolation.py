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

from unittest import TestCase

from eao_util import interpolation


class InterpolationTest(TestCase):
    def test_compress_list(self):
        in_ = [
            (1, 10),
            (2, 11),
            (3, 10),
            (4, 9),
            (5, 10),
        ]

        out = interpolation.compress_list(in_, tolerance=0.1)

        self.assertEqual(out, [
            (1, 10),
            (2, 11),
            (4, 9),
            (5, 10),
        ])

        out = interpolation.compress_list(in_, tolerance=2.0)

        self.assertEqual(out, [
            (1, 10),
            (5, 10),
        ])
