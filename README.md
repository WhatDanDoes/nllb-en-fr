nllb-en-fr
==========

This project leverages the software developed by Meta's _No Language Left Behind_ initiative: https://github.com/facebookresearch/fairseq/tree/nllb.

I wrapped the Meta software in a `python` command-line script and used it to the translate the King James Version of the Holy Bible from 1611 into modern French, German, and Russian using the same publicly-available pre-trained models as the NLLB researchers. The `python` script and tests are geared for French. If you're interested in repeating the German and Russian translations, these will require manual ad hoc adjustments to the code in `en_to_fr/command.py`.

Heads up! Regular `python` developers may find this all a bit cringy. This project was the first time I'd used `python` in ten years. I am still not really familiar with the tools and culture of the `python` ecosystem.

_Note to self:_ if you're trying to get the tests to pass, make sure you reinstall the module after every change: `pip install .` (super hokey, I know. What's the right way to do this?).

# Setup

Set up instructions have been adapted from: https://github.com/facebookresearch/fairseq/blob/nllb/INSTALL.md

## Virtual Environments

From https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

Create:

```
venv env
```

Activate:

```
source env/bin/activate
```

Deactivate (as appropriate):

```
deactivate
```

## Install Dependencies

Install the NLLB-specific NLLB dependencies before installing project-wide dependencies. All dependent ad-hoc dependencies are stored in this directory:

```
cd nllb
```

### Fairseq NLLB Dependencies

#### Apex

This assumes your NVIDIA GPU has been setup properly.

```
git clone https://github.com/NVIDIA/apex.git
cd apex
git checkout e2083df5eb96643c61613b9df48dd4eea6b07690
pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" --global-option="--deprecated_fused_adam" --global-option="--xentropy" --global-option="--fast_multihead_attn" ./
```

Once installed, navigate back to this project's `nllb/` directory:

```
cd ..
```

#### Megatron

```
git clone --depth=1 --branch v2.4 https://github.com/NVIDIA/Megatron-LM.git
cd Megatron-LM
pip install -e .
cd ..
```

#### Fairscale

```
git clone https://github.com/facebookresearch/fairscale.git
cd fairscale
# needed when loading MoE checkpoint w/num_experts < num_gpus
git checkout origin/experts_lt_gpus_moe_reload_fix
pip install -e .
cd ..
```

#### Fairseq NLLB Branch

```
git clone https://github.com/facebookresearch/fairseq.git
cd fairseq
git checkout nllb
pip install -e .
python setup.py build_ext --inplace
cd ..
```

#### Stopes

```
git clone https://github.com/facebookresearch/stopes.git
cd stopes
pip install -e '.[dev]'
```

#### Pre-commit Hooks

Finally, go back to the root of the project directory,

```
cd ../..
```

**I'm not sure this is actually necessary, given what little I know of _pre-commit hooks_**

And execute the following:

```
# turn on pre-commit hooks
pip install pre-commit && pre-commit install
```

### Project Dependencies

**In retrospect, having manually installed all the NLLB dependencies above, I've discovered those steps might not be necessary. It all may be encompassed in the following step**

```
pip install -r requirements.txt
```

## Model data

### NLLB

As per https://github.com/facebookresearch/fairseq/blob/nllb/examples/nllb/data/README.md

Had to install a couple more dependencies:

```
pip install openpyxl translate-toolkit
```

Obtained thusly:

```
python ./env/src/fairseq/examples/nllb/data/download_parallel_corpora.py --directory ./models
```

### Neural Machine Translation

As per https://github.com/facebookresearch/fairseq/tree/nllb/examples/translation

Whatever was obtained from there was downloaded manually and saved in `models/nm-translation`.

Note the difference between the _convolution_ and _transformer_ models:

https://towardsdatascience.com/is-this-the-end-for-convolutional-neural-networks-6f944dccc2e9

This is another neat one:

https://towardsdatascience.com/transformers-in-computer-vision-farewell-convolutions-f083da6ef8ab

# Testing

```
make test
```

Testing a single test:

```
pytest tests/test_command.py -k 'test_digit_skipping'
```

For future me, this is causing some momentary frustration. The module has to be installed before it'll be properly tested. Changes made to the file don't register for some reason. I'm sure this isn't how it's supposed to be done:

```
pip install .
```

# Processing a directory of JSON

This is where the actual translation took place. Nothing fancy. Just a `bash` command to execute over a directory of structured Bible data obtained from [here](https://github.com/aruljohn/Bible-kjv).

```
mkdir out/data
find data -name "*.json" -type f -exec sh -c 'en_to_fr --json {} > out/{}' \;
```

The original output is preserved in the `out/` directory. No doubt, translating antiquated English into modern languages is a little weird.

Execution times using an Nvidia GeForce RTX GPU:

- French - 10.5 hours
- German - 8.5 hours
- Russian - 33 hours

