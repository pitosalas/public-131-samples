import unittest
import hypothesis.strategies as st
from hypothesis import given
from lib.pagetables import TwoLevelPageTable 
from lib.utils import collapse_contiguous_ranges, check_number_in_range, find_free_sequence


class TestVarSegPhysMem(unittest.TestCase):
    @given(st.integers(), st.integers())
    def test_ints_are_commutative(self, x, y):
        assert x + y == y + x

    @given(st.lists(st.integers()))
    def test_collapse_contiguous_ranges(self, range: list[int]):
        collapsed = collapse_contiguous_ranges(range)
        for i in range:
            assert check_number_in_range(i, collapsed)

    @given(st.integers(min_value=1, max_value=2**16), st.integers(min_value=1, max_value=2**16))
    def test_hyp_sparse_frame(self, pagesize: int, frame_count: int):
        spt = TwoLevelPageTable(pagesize, frame_count)
        for i in range(frame_count):
            spt.set_frame(i, i)
        for i in range(frame_count):
            assert spt.get_frame(i) == i

    @given(st.lists(st.integers()), st.integers(), st.integers())
    def test_find_free_sequence(self, lst: list[int], target: int, n: int):
        result = find_free_sequence(lst, target, n)
        if result is not None:
            assert result[1] - result[0] == n
            assert all(x is target for x in lst[result[0]:result[1]])
