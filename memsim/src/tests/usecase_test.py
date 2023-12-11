import unittest
from lib.mm_fixed_seg import FixedSegMm
from lib.mm_var_seg import VarSegMm


class UseCaseTest(unittest.TestCase):
    def setUp(self):
        self.param = {
            "proportion_allocated": 0.5,
            "script": [["a", "p1", "4"]],
            "algo": {"name": "paged", "page_size": 2048},
            "memory": {
                "base_units": "hex",
                "size": {"size": 1, "multiplier": "2**16"},
                "seg": {"size": 1, "multiplier": "2**12"},
            },
        }
        self.fixedseg_mm = FixedSegMm(self.param)
        self.varseg_mm = VarSegMm(self.param)

    def test_created(self):
        self.assertIsNotNone(self.fixedseg_mm)
        self.assertIsNotNone(self.varseg_mm)

    def test_alocation(self):
        self.fixedseg_mm.allocate("p1", 4096)
        allocation = self.fixedseg_mm.allocations["p1"]
        self.assertEqual(allocation.mapping.size, 4096)

        self.varseg_mm.allocate("p1", 4096)
        self.assertEqual(allocation.mapping.size, 4096)

    def test_touch(self):
        self.fixedseg_mm.allocate("p1", 4096)
        self.assertEqual(self.fixedseg_mm.touch("p1", 200), True)

        self.varseg_mm.allocate("p1", 4096)
        self.assertEqual(self.fixedseg_mm.touch("p1", 200), True)
