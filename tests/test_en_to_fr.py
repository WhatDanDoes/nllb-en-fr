
# From https://www.youtube.com/watch?v=6tNS--WetLI

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import unittest
import en_to_fr
#from .context import en_to_fr

class TestCase(unittest.TestCase):

  def test_add(self):

    self.assertEqual(en_to_fr.add(10, 5), 15)
    self.assertEqual(en_to_fr.add(-1, 1), 0)
    self.assertEqual(en_to_fr.add(-1, -1), -2)

# This makes it so I don't have to pass the unittest module from the commandline
#if __name__ == '__main__':
#    unittest.main()


