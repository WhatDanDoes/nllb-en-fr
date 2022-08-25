import re

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
  out = en2fr.translate(phrase)

  # The NLLB stuff puts unwantedspaces between punctuation and words
  #
  # From https://stackoverflow.com/a/35141903
  fix_spaces = re.compile(r'\s*([?!.,]+(?:\s+[?!.,]+)*)\s*')
  out = fix_spaces.sub(lambda x: "{} ".format(x.group(1).replace(" ", "")), out).strip()

  return out
