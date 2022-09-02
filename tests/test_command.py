
import pytest
import en_to_fr.command

def test_translate_single_word():
  """
  Simple sanity check to ensure I've figured out how to test with Python
  """
  assert en_to_fr.command.translate("Hello") == "Bonjour"

def test_translate_sentence():
  """
  Translate an entire sentence and correct punctuation spacing, escaped HTML, and other oddities
  """
  assert en_to_fr.command.translate("In the beginning God created the heaven and the earth.") == "Au commencement, Dieu créa le ciel et la terre."
  assert en_to_fr.command.translate("I'm going to Grandpa's house, probably") == "Je vais à la maison des grands-parents, probablement"
  assert en_to_fr.command.translate("This is a test") == "Il s'agit d'un test"
  assert en_to_fr.command.translate("I walked up to the lake") == "J'ai marché jusqu'au lac"
  assert en_to_fr.command.translate("Do you want to come this weekend?") == "Voulez-vous venir cette fin de semaine?"


def test_translate_json_file():
  """
  Take an ad-hoc JSON file and translate its contents
  """
  # Also defined in test_cli. Super hokey
  expected_json = '{"book": "Mon livre", "chapters": [{"chapter": "1", "verses": [{"verse": "1", "text": "C\'est mon livre."}, {"verse": "2", "text": "De quoi s\'agit-il?"}]}]}'

  result = en_to_fr.command.translate_json('tests/data/book.json')
  assert result == expected_json
