"""
Packaging for Meta's NLLB translator wrapper
"""
from pathlib import Path

import en_to_fr as package
from setuptools import find_packages, setup


def read_file(filename):
    """Read a text file and return its contents."""
    project_home = Path(__file__).parent.resolve()
    file_path = project_home / filename
    return file_path.read_text(encoding="utf-8")


setup(
    name='en_to_fr',
    version=package.__version__,
    description=package.__doc__.strip().split('\n', maxsplit=1)[0],
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Daniel Bidulock',
    author_email='daniel@bscc.dev',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'en_to_fr = en_to_fr.cli:main',
        ],
    },
)
