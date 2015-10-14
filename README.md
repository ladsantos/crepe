# CREPE

CRoss-Entropy Parameter Estimation is a project aiming to create a simple yet powerful global optimization tool.

Installation
------------

CREPE is compatible with Python 2.7. Compatibility with other versions of Python is not yet verified. Required packages: 'nose', 'numpy'. Recommended packages: 'matplotlib', 'pip'.

Use git to grab the latest version of CREPE (you might need administrative rights to install it - in that case, use sudo):

    git clone https://github.com/laugustogs/crepe.git
    cd crepe
    python setup.py install

Changelog:
------------

* 0.1.151014: added docstrings
* 0.1.150822: corrected an incorrect implementation of the I matrix (which selects the elite sample). It was missing a [0].
* 0.1.150822: CREPE now uses the lower limit in sigma as a test for convergence

To be added in the future:
------------

* docs.Manual: Hacks to avoid falling in local minima
* crepe: Creating standard performance functions
* crepe: Multi-variate gaussian distributions
