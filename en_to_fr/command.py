import re
import html
import json

#
# From https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
#
# This squelches all the stdout, stderr clutter coming from the NLBB stuff
#
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

# 2022-8-31 How does this work? Shouldn't the `en2fr` var be out of scope?
#en2fr = Null
with suppress_stdout_stderr():
  from fairseq.models.transformer import TransformerModel
  #
  # This is all pre-wired for translating French
  #
  en2fr = TransformerModel.from_pretrained(
    #
    # French (default)
    #
    './models/nm-translation/wmt14.en-fr.joined-dict.transformer/',
    checkpoint_file='model.pt',
    bpe='subword_nmt',
    bpe_codes='bpecodes'

    #
    # German
    #
    #'./models/nm-translation/wmt16.en-de.joined-dict.transformer/',
    #checkpoint_file='model.pt',
    #bpe='subword_nmt',
    #bpe_codes='bpecodes'

    #
    # Russian
    #
    #'./models/nm-translation/wmt19.en-ru.ensemble/',
    #checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
    #tokenizer='moses',
    #bpe='fastbpe',
    #bpe_codes='bpecodes'

    #
    # What is this?
    #
    # It's in the provided project examples, but it doesn't seem to affect
    # anything
    #
    #data_name_or_path='data-bin/wmt14_en_fr_full',
  )


#
# From https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
#
# Don't translate standalone parsable floats
#
def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

def translate(phrase):
  """
  Translate a phrase from English to French
  """
  with suppress_stdout_stderr():

    # Skip standalone float-parsable digits
    if is_float(phrase):
      return phrase

    out = en2fr.translate(phrase)

    # The `translate` method produces escaped HTML strings
    out = html.unescape(out)

    # The NLLB stuff puts unwanted spaces between punctuation and words
    #
    # From https://stackoverflow.com/a/35141903
    fix_spaces = re.compile(r'\s*([?!.,:;]+(?:\s+[?!.,:;]+)*)\s*')
    out = fix_spaces.sub(lambda x: "{} ".format(x.group(1).replace(" ", "")), out).strip()

    # Fix apostrophes
    fix_apostrophes = re.compile(r"\s*([']+(?:\s+[']+)*)\s*")
    out = fix_apostrophes.sub(lambda x: "{}".format(x.group(1).replace(" ", "")), out).strip()

    # Fix dashes. `translate` makes them look like this ' @-@ '
    out = re.sub(r" @-@ ", "-", out)

    return out


def translate_json(filepath):
  """
  Take an ad-hoc JSON file and translate its contents
  """
  with open(filepath) as f:
    data = json.load(f)

  return recurse_keys(data)


def recurse_keys(current_obj):
  """
  Take the JSON, traverse it all keys, translate whatever values you find
  """
  if isinstance(current_obj, dict):
    # Another dictionary to search through
    for k,v in current_obj.items():

      if (isinstance(current_obj[k], dict) or isinstance(current_obj[k], list)):
        recurse_keys(current_obj[k])
      else:
        current_obj[k] = translate(v)
  elif isinstance(current_obj, list):
    for i in current_obj:
      if isinstance(i, dict) or isinstance(i, list):
        recurse_keys(i)
      else:
        current_obj[k] = recurse_keys(i)

  return json.dumps(current_obj)


