import unittest

from hypothesis import given
import hypothesis.strategies as st

from lib.pagetables import PageTable
from lib.pm_paged import PagedPm


class PageTableTest(unittest.TestCase):
    def test_pagetable_1(self):
        params = {
            "algo": {"name": "paged", "page_size": 1024},
            "memory": {"size": {"size": 4, "multiplier": "2**10"}},
        }
        physmem = PagedPm(params)
        pt = PageTable("P1", physmem)
        pt.allocate(1 * 2**10)
        pt.allocate(2 * 2**10)
        assert physmem.free_frames() == 0
        assert pt.frame_count == 3
        
    @given(st.integers(min_value=1, max_value=12), st.integers(min_value=1, max_value=12), st.integers(min_value=1, max_value=31))
    def test_pagetable_hypo(self, block1: int, block2: int, block3: int):
        tot_frames = block1 + block2 + block3 + 2
        params = {
            "algo": {"name": "paged", "page_size": 1024},
            "memory": {"size": {"size": tot_frames, "multiplier": "2**10"}},
        }
        physmem = PagedPm(params)
        pt = PageTable("P1", physmem)
        pt.allocate(block1 * 2**10)
        pt.allocate(block2 * 2**10)
        pt.allocate(block3 * 2**10)
        assert physmem.free_frames() == 1
        assert pt.frame_count == block1 + block2 + block3