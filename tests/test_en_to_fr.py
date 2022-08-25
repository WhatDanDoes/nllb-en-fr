# From https://www.youtube.com/watch?v=6tNS--WetLI

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import pytest
import en_to_fr

def test_translate_single_word():
  """
  Simple sanity check to ensure I've figured out how to test with Python
  """
  assert en_to_fr.translate("Hello") == "Bonjour"

def test_translate_sentence():
  """
  Translate an entire sentence and correct punctuation spacing
  """
  assert en_to_fr.translate("In the beginning God created the heaven and the earth.") == "Au commencement, Dieu créa le ciel et la terre."



