import unittest

from memory_managers import VarSegMm


class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory_param = {"size": 2, "multiplier": "2**12"}
        self.memory_manager = VarSegMm(memory_param=self.memory_param)

    def test_allocate(self):
        self.memory_manager.allocate(process="process1", size=10)
        self.assertIn("process1", self.memory_manager.allocations)

    def test_deallocate(self):
        self.memory_manager.allocate(process="process1", size=10)
        self.memory_manager.deallocate(process="process1")
        self.assertNotIn("process1", self.memory_manager.allocations)

    def test_allocate_deallocate(self):
        self.memory_manager.allocate(process="process1", size=15)
        self.memory_manager.deallocate(process="process1")
        self.assertNotIn("process1", self.memory_manager.allocations)