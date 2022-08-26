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
  Translate an entire sentence and correct punctuation spacing, escaped HTML, and other oddities
  """
  assert en_to_fr.translate("In the beginning God created the heaven and the earth.") == "Au commencement, Dieu créa le ciel et la terre."
  assert en_to_fr.translate("I'm going to Grandpa's house, probably") == "Je vais à la maison des grands-parents, probablement"
  assert en_to_fr.translate("This is a test") == "Il s'agit d'un test"
  assert en_to_fr.translate("I walked up to the lake") == "J'ai marché jusqu'au lac"
  assert en_to_fr.translate("Do you want to come this weekend?") == "Voulez-vous venir cette fin de semaine?"



