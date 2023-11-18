import unittest

from physical_memory import FixedSegPhysMem, PagedPhysMem, VarSegPhysMem
from utils import convert_size_with_multiplier


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


class TestFixedSegPhysMem(unittest.TestCase):
    def setUp(self):
        self.fixed_param = {
            "memory": {
                "size": {"size": 10, "multiplier": "2**16"},
                "seg": {"size": 1, "multiplier": "2**16"},
            }
        }
        self.mem_size = 10 * 2**16
        self.seg_size = 1 * 2**16
        self.mem = FixedSegPhysMem(self.fixed_param)

    def test_initialization(self):
        self.assertEqual(self.mem.memsize, self.mem_size)
        self.assertEqual(self.mem.segsize, self.seg_size)
        self.assertEqual(len(self.mem.free_segments), self.mem_size // self.seg_size)

    def test_allocate_deallocate(self):
        size = 1
        block = self.mem.allocate("Test1", size)
        self.assertIsNotNone(block)
        self.assertEqual(block.size, size)

        initial_free_segments = len(self.mem.free_segments)
        self.mem.deallocate(block)
        self.assertEqual(
            len(self.mem.free_segments),
            initial_free_segments + (size // self.mem.segsize),
        )


class TestPagedPhysMem(unittest.TestCase):
    def setUp(self):
        self.mem_size = 1 * 2**30
        self.page_size = 4096
        self.paged = {"memory": {"size": {"size": 10, "multiplier": "2**16"}}}
        self.mem = PagedPhysMem(self.paged, self.page_size)

    def test_initialization(self):
        mem_size_bytes = convert_size_with_multiplier(self.paged["memory"]["size"])
        self.assertEqual(self.mem.memsize, mem_size_bytes)
        self.assertEqual(self.mem.pagesize, self.page_size)
        self.assertEqual(len(self.mem.frame_table), mem_size_bytes // self.page_size)

    def test_allocate_deallocate(self):
        size = 8192  # 2 pages
        process = "test_process"
        page_table = self.mem.allocate(process, size)
        self.assertIsNotNone(page_table)
        self.assertEqual(len(page_table.table), 2)

        initial_frame_count = sum(1 for frame in self.mem.frame_table if frame is None)
        self.mem.deallocate(page_table)
        new_frame_count = sum(1 for frame in self.mem.frame_table if frame is None)
        self.assertEqual(new_frame_count, initial_frame_count + 2)


if __name__ == "__main__":
    unittest.main()
