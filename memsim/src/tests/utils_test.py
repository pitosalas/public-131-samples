import unittest
from lib.utils import extract_fields, find_and_remove, collapse_contiguous_ranges
from collections import Counter


class TestFindAndRemove(unittest.TestCase):
    def test1(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 3
        expected_output = [[1, 2, 3], [4, 5, 6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test2(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 5
        expected_output = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test3(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 10
        expected_output = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], []]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test4(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 1
        expected_output = [[1], [2, 3, 4, 5, 6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test5(self):
        lst = [1, 2, 3, 5, 6, 7, 8, 9, 10]
        n = 3
        expected_output = [[1, 2, 3], [5, 6, 7, 8, 9, 10]]
        result = find_and_remove(lst, n)
        self.assertTrue(check_lists(lst, result[0], result[1]))
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test6(self):
        lst = [1, 2, 3, 5, 6, 7, 8, 9, 10]
        n = 11
        self.assertEqual(find_and_remove(lst, n), None)


class TestFlattenFree(unittest.TestCase):
    def test7(self):
        free_segments = [1, 2, 3, 5, 6, 7, 8, 10, 11, 12]
        expected_output = [(1, 3), (5, 8), (10, 12)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)

    def test8(self):
        free_segments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected_output = [(1, 10)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)

    def test9(self):
        free_segments = [1, 3, 5, 7, 9]
        expected_output = [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)

    def test10(self):
        free_segments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        expected_output = [(1, 12)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)

    def test11(self):
        free_segments = [1, 3, 5, 7, 9, 11]
        expected_output = [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9), (11, 11)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)

    def test12(self):
        free_segments = [1, 3]
        expected_output = [(1, 1), (3, 3)]
        self.assertEqual(collapse_contiguous_ranges(free_segments), expected_output)


class UtilsTest(unittest.TestCase):
    def test_extract_fields1(self):
        inner = 2
        outer = 2
        offset = 35
        address = (outer << 20) + (inner << 8) + offset
        outer_page_number, inner_page_number, page_offset = extract_fields(
            address, 12, 12, 8
        )
        print(outer_page_number, inner_page_number, page_offset)
        assert (
            outer_page_number == outer
            and inner_page_number == inner
            and page_offset == offset
        )


def check_lists(list1, list2, list3):
    c1 = Counter(list1)
    c2 = Counter(list2)
    c3 = Counter(list3)
    c2 |= c3
    return all(value == c2[elem] for elem, value in c1.items())
