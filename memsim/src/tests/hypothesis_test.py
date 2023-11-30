import unittest

import hypothesis.strategies as st
from hypothesis import given
from lib.utils import collapse_contiguous_ranges, check_number_in_range

class TestVarSegPhysMem(unittest.TestCase):

    @given(st.integers(), st.integers())
    def test_ints_are_commutative(x, y):
        assert x + y == y + x


    @given(st.lists(st.integers()))
    def test_collapse_contiguous_ranges(range: list[int]):
        collapsed = collapse_contiguous_ranges(range)
        for i in range:
            assert check_number_in_range(i, collapsed)

        assert collapse_contiguous_ranges(range) == [range[0], range[-1]]

