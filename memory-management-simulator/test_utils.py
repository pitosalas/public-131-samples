import unittest
from utils import find_and_remove


class TestUtils(unittest.TestCase):
    def test1(self):
        # Test case 1
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 3
        expected_output = [[1, 2, 3], [4, 5, 6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test2(self):
        # Test case 2
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 5
        expected_output = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test3(self):
        # Test case 3
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 10
        expected_output = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], []]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test4(self):
        # Test case 4
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 1
        expected_output = [[1], [2, 3, 4, 5, 6, 7, 8, 9, 10]]
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test5(self):
        # Test case 5
        lst = [1, 2, 3, 5, 6, 7, 8, 9, 10]
        n = 3
        expected_output = [[1, 2, 3], [5, 6, 7, 8, 9, 10]]
        result = find_and_remove(lst, n)
        self.assertTrue(check_lists(lst, result[0], result[1]))
        self.assertEqual(find_and_remove(lst, n), expected_output)

    def test6(self):
        # Test case 5
        lst = [1, 2, 3, 5, 6, 7, 8, 9, 10]
        n = 11
        expected_output = [[1, 2, 3], [5, 6, 7, 8, 9, 10]]
        result = find_and_remove(lst, n)
        self.assertEqual(find_and_remove(lst, n), None)




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
