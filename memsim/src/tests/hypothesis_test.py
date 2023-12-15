import unittest
import hypothesis.strategies as st
from hypothesis import given
from lib.utils import collapse_contiguous_ranges, check_number_in_range, extract_fields, find_free_sequence


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
# sourcery skip: no-conditionals-in-tests
        if result is not None:
            assert result[1] - result[0] == n
            assert all(x == target for x in lst[result[0]:result[1]])

    @given(st.integers(min_value=1, max_value=12), st.integers(min_value=1, max_value=12), st.integers(min_value=1, max_value=31))
    def test_extract_fields(self, outer, inner, offset):
# sourcery skip: no-conditionals-in-tests
        if outer + inner + offset > 32:
            return
        address = (outer << 20) + (inner << 8) + offset
        outer_page_number, inner_page_number, page_offset = extract_fields(address, 12, 12, 8)
        print(outer_page_number, inner_page_number, page_offset)
        assert outer_page_number == outer and inner_page_number == inner and page_offset == offset           