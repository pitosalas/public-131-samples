import unittest
import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings
from lib.utils import collapse_contiguous_ranges, check_number_in_range
from lib.utils import SparsePageTable


class TestVarSegPhysMem(unittest.TestCase):
    @given(st.integers(), st.integers())
    def test_ints_are_commutative(self, x, y):
        assert x + y == y + x

    @given(st.lists(st.integers()))
    def test_collapse_contiguous_ranges(self, range: list[int]):
        collapsed = collapse_contiguous_ranges(range)
        for i in range:
            assert check_number_in_range(i, collapsed)

    @given(st.lists(st.integers()), st.integers())
    def test_hyp_sparse_frame(self, pagesize: int, frame_count: int):
        spt = SparsePageTable(pagesize, frame_count)
        for i in range(frame_count):
            spt.set_frame(i, i)
        for i in range(frame_count):
            assert spt.get_frame(i) == i

