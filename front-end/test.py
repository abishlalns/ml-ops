import unittest

class unitTesting(unittest.TestCase):
    def test_demo__1(self):
        self.assertEqual(1, 1)
        print('demo_1')
    def test_demo_2(self):
        self.assertEqual(1, 1)
        print('demo_2')
    def test_demo_3(self):
        self.assertEqual(1, 2)
        print('demo_3')
    def test_demo_4(self):
        self.assertEqual(1, 1)
        print('demo_4')
    def test_demo_5(self):
        self.assertEqual(1, 1)
        print('demo_5')


if __name__ == '__main__':
    unittest.main()