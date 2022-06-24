#!/usr/bin/env python3

import unittest
from conan_create_changed import *

class TestMethods(unittest.TestCase):
    def test_get_recipe_name(self):
        self.assertEqual(get_recipe_name(""), "")
        self.assertEqual(get_recipe_name("zlib/1.2.12"), "zlib")
        self.assertEqual(get_recipe_name("conanfile.py (libpng/1.6.37)"), "libpng")


if __name__ == '__main__':
    unittest.main()
