
import pytest
import json
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
  assert en_to_fr.command.translate("And the earth was without form, and void;") == "Et la terre était sans forme, et nulle;"
  assert en_to_fr.command.translate("And God said, Let there be light: and there was light.") == "Dieu a dit: Que la lumière soit, et la lumière était."


def test_translate_json_file():
  """
  Take an ad-hoc JSON file and translate its contents
  """
  # Also defined in test_cli. Super hokey
  expected_json = '{"book": "Mon livre", "chapters": [{"chapter": "1", "verses": [{"verse": "1", "text": "C\'est mon livre."}, {"verse": "2", "text": "De quoi s\'agit-il?"}]}]}'

  result = en_to_fr.command.translate_json('tests/data/book.json')
  assert result == expected_json

def test_is_float():
  """
  Determine if the provided value is numeric (parsable as a float)
  """
  assert en_to_fr.command.is_float('15') == True
  assert en_to_fr.command.is_float('26') == True
  assert en_to_fr.command.is_float('32 blue') == False
  assert en_to_fr.command.is_float('Forty two') == False


def test_digit_skipping():
  """
  NLLB will try to translate digits, which doesn't always work out. This tests
  to ensure standalone (float parsable) digit values are skipped. A few of the
  most problematic are tested below
  """
  result = en_to_fr.command.translate_json('tests/data/digits.json')
  data = json.loads(result)

  assert data['chapters'][0]['chapter'] == '15'
  assert data['chapters'][1]['chapter'] == '26'
  assert data['chapters'][2]['chapter'] == '132'



