import unittest

from lib.pm_fixed_seg import FixedSegPhysMem


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
