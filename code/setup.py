
from setuptools import setup, find_packages
import os 

VERSION = '0.0.1'
DESCRIPTION = 'An easy class for a quantum key distribution (BB84) protocol'
LONG_DESCRIPTION = 'An easy class showing the efficiency of BB84 protocol with a detailed focus on the detection probability due to an eavesdropper within the communication.'

# Setting 
setup(
    name='QKD',
    version=VERSION,
    author='Francesco Aldo Venturelli',
    author_email='francesco.venturell3@studio.unibo.it',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['qiskit', 'numpy', 'matplotlib'],
    keywords=['python','qiskit','quanutm','cryptography'],
    classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    ]
)
