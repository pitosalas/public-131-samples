import unittest
from utils import find_and_remove, flatten_free_segments


class TestFindAndREmove(unittest.TestCase):
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
        self.assertEqual(flatten_free_segments(free_segments), expected_output)

    def test8(self):
        free_segments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected_output = [(1, 10)]
        self.assertEqual(flatten_free_segments(free_segments), expected_output)

    def test9(self):
        free_segments = [1, 3, 5, 7, 9]
        expected_output = [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9)]
        self.assertEqual(flatten_free_segments(free_segments), expected_output)

    def test10(self):
        free_segments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        expected_output = [(1, 12)]
        self.assertEqual(flatten_free_segments(free_segments), expected_output)

    def test11(self):
        free_segments = [1, 3, 5, 7, 9, 11]
        expected_output = [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9), (11, 11)]
        self.assertEqual(flatten_free_segments(free_segments), expected_output)

    def test12(self):
        free_segments = [1, 3]
        expected_output = [(1, 1), (3, 3)]
        self.assertEqual(flatten_free_segments(free_segments), expected_output)


def check_lists(list1, list2, list3):
    from collections import Counter

    c1 = Counter(list1)
    c2 = Counter(list2)
    c3 = Counter(list3)
    c2.update(c3)
    for elem in c1:
        if c1[elem] != c2[elem]:
            return False
    return True


if __name__ == "__main__":
    unittest.main()
