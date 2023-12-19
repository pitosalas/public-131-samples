import unittest
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
        

