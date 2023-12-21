import unittest
from lib.pm_fixed_seg import FixedSegPhysMem
from lib.pm_paged import PagedPm
from lib.pm_var_seg import VarSegPhysMem

from lib.utils import convert_size_with_multiplier


class TestVarSegPhysMem(unittest.TestCase):
    def setUp(self):
        self.mem_size_gig = 1
        self.param = {"memory": {"size": {"size": 1, "multiplier": "2**30"}}}

        self.mem = VarSegPhysMem(self.param)

    def test_initialization(self):
        expected_size = self.mem_size_gig * 2**30
        self.assertEqual(self.mem.size, expected_size)
        self.assertEqual(len(self.mem.freelist), 1)
        self.assertEqual(self.mem.freelist[0].size, expected_size)

    def test_allocate_deallocate(self):
        size = 1024
        block = self.mem.allocate(size)
        self.assertIsNotNone(block)
        self.assertEqual(block.size, size)

        initial_free_memory = self.mem.free_memory()
        self.mem.deallocate(block)
        self.assertEqual(self.mem.free_memory(), initial_free_memory + size)

    def test_coalescing(self):
        block1 = self.mem.allocate(1024)
        block2 = self.mem.allocate(2048)
        self.mem.deallocate(block1)
        self.mem.deallocate(block2)

        # Assuming coalescing happens in deallocate
        self.assertEqual(len(self.mem.freelist), 1)
        self.assertEqual(self.mem.freelist[0].size, 1 * 2**30)


class TestPagedPhysMem(unittest.TestCase):
    def setUp(self):
        self.mem_size = 1 * 2**30
        self.paged = {
            "memory": {"size": {"size": 10, "multiplier": "2**10"}},
            "algo": {"page_size": 1024},
        }
        self.mem = PagedPm(self.paged)

    def test_initialization(self):
        mem_size_bytes = convert_size_with_multiplier(self.paged["memory"]["size"])
        self.assertEqual(self.mem.memsize, mem_size_bytes)
        self.assertEqual(
            len(self.mem.frame_table), mem_size_bytes // self.paged["algo"]["page_size"]
        )

    def test_allocate_deallocate(self):
        size = 1024  # 1 pages
        process = "test_process"
        page_table = self.mem.allocate(process, size)
        self.assertIsNotNone(page_table)
        self.assertEqual(len(page_table.table), 1)

        initial_frame_count = sum(frame is None for frame in self.mem.frame_table)
        self.mem.deallocate(page_table)
        new_frame_count = sum(frame is None for frame in self.mem.frame_table)
        self.assertEqual(new_frame_count, initial_frame_count + 1)


if __name__ == "__main__":
    unittest.main()
