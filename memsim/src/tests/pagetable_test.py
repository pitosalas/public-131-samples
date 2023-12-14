import unittest

from lib.pagetables import TwoLevelPageTable

class PageTableTest(unittest.TestCase):

    def test_binary_fields(self):
        two_level_page_table = TwoLevelPageTable( 2**10-1, 1*2**20)
        inner = 0
        outer = 0
        offset = 256
        address = (outer << 22) + (inner << 12) + offset
        two_level_page_table.extract_fields(address)
        outer_page_number, inner_page_number, page_offset = two_level_page_table.extract_fields(address)
        assert outer_page_number == outer and inner_page_number == inner and page_offset == offset
        


