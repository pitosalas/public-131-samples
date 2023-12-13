import unittest
import hypothesis.strategies as st
from hypothesis import given
from lib.pagetables import TwoLevelPageTable 
from lib.utils import collapse_contiguous_ranges, check_number_in_range, find_free_sequence


class Hypotheses(unittest.TestCase):
    @given(st.integers(), st.integers())
    def test_ints_are_commutative(self, x, y):
        assert x + y == y + x

    @given(st.lists(st.integers()))
    def test_collapse_contiguous_ranges(range: list[int]):
        collapsed = collapse_contiguous_ranges(range)
        assert all(check_number_in_range(i, collapsed) for i in range)


    @given(st.lists(st.integers()), st.integers(), st.integers())
    def test_find_free_sequence(self, lst: list[int], target: int, n: int):
        result = find_free_sequence(lst, target, n)
        if result is not None:
            assert result[1] - result[0] == n
            assert all(x == target for x in lst[result[0]:result[1]])

    @given(st.lists(st.integers(min_value=0, max_value=2047), min_size=1, max_size=3))
    def test_two_level_page_table(self, access_list):
        two_level_page_table = TwoLevelPageTable( 4*2**10-1, 1*2**20)
        assert all(two_level_page_table.access(x)=="allocated" for x in access_list)

    @given(st.integers(min_value=0, max_value=2**10-1), st.integers(min_value=0, max_value=2**10-1), st.integers(min_value=0, max_value=4*2**10-1))  
    def test_extract_fields(self, outer_pt, inner_pt, offset):
        # Create an instance of the class
        try:
            two_level_page_table = TwoLevelPageTable( 4*2**10-1, 1*2**20)
        except ValueError:
            return
        address = (outer_pt << 22) + (inner_pt  << 12) + offset
        assert two_level_page_table.extract_fields(address) == (outer_pt, inner_pt, offset)

