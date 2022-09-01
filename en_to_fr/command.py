import re
import html

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
  en2fr = TransformerModel.from_pretrained(
    './models/nm-translation/wmt14.en-fr.joined-dict.transformer/',
    checkpoint_file='model.pt',
    # What is this?
    #data_name_or_path='data-bin/wmt14_en_fr_full',
    bpe='subword_nmt',
    bpe_codes='bpecodes'
  )


def translate(phrase):
  """
  Translate a phrase from English to French
  """

  with suppress_stdout_stderr():
    out = en2fr.translate(phrase)

    # The `translate` method produces escaped HTML strings
    out = html.unescape(out)

    # The NLLB stuff puts unwanted spaces between punctuation and words
    #
    # From https://stackoverflow.com/a/35141903
    fix_spaces = re.compile(r'\s*([?!.,]+(?:\s+[?!.,]+)*)\s*')
    out = fix_spaces.sub(lambda x: "{} ".format(x.group(1).replace(" ", "")), out).strip()

    # Fix apostrophes
    fix_apostrophes = re.compile(r"\s*([']+(?:\s+[']+)*)\s*")
    out = fix_apostrophes.sub(lambda x: "{}".format(x.group(1).replace(" ", "")), out).strip()

    # Fix dashes. `translate` makes them look like this ' @-@ '
    out = re.sub(r" @-@ ", "-", out)

    return out


