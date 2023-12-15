import unittest
from lib.utils import extract_fields

class UtilsTest2(unittest.TestCase):
    def test_extract_fields1(self):
        inner = 2
        outer = 2
        offset = 35
        address = (outer << 20) + (inner << 8) + offset
        outer_page_number, inner_page_number, page_offset = extract_fields(address, 12, 12, 8)
        print(outer_page_number, inner_page_number, page_offset)
        assert outer_page_number == outer and inner_page_number == inner and page_offset == offset        
