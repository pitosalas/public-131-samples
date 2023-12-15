import unittest
from lib.mm_fixed_seg import FixedSegMm
from lib.mm_paged import PagedMm
from lib.mm_var_seg import VarSegMm

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.json_file = {
            "memory": {
                "size": {"size": 2, "multiplier": "2**20"},
                "seg": {"size": 1, "multiplier": "2**12"},
            },
            "default_multiplier": "2**10",
            "algo": { "page_size": 2048 }
        }
        self.varsegmm = VarSegMm(memory_param=self.json_file)
        self.fixedsegmm = FixedSegMm(memory_param=self.json_file)
        self.pagedmm = PagedMm(memory_param=self.json_file)
        self.multiplier = eval(self.json_file["default_multiplier"])

    def test_allocate(self):
        self.allocate(self.varsegmm)
        self.allocate(self.fixedsegmm)
        self.allocate(self.pagedmm)

    def allocate(self, mm):
        mm.allocate(process="process1", size=10 * self.multiplier)
        self.assertIn("process1", mm.allocations)
        self.assertEqual(mm.allocations["process1"].mapping.size, 10 * self.multiplier)

    def test_deallocate(self):
        self.deallocate(self.varsegmm)
        self.deallocate(self.fixedsegmm)

    def deallocate(self, mm):
        mm.allocate(process="process1", size=10)
        mm.deallocate(process="process1")
        self.assertNotIn("process1", mm.allocations)

    def test_allocate_deallocate(self):
        self.allocate_deallocate(self.varsegmm)
        self.allocate_deallocate(self.fixedsegmm)

    def allocate_deallocate(self, mm):
        mm.allocate(process="process1", size=10)
        mm.deallocate(process="process1")
        self.assertNotIn("process1", mm.allocations)
