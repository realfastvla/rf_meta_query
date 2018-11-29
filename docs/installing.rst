.. highlight:: rest

************************
Installing rf_meta_query
************************

This document describes how to install the `rf_meta_query`
repository.  We also describe
:ref:`download-public`.

Installing Dependencies
=======================
We have and will continue to keep the number of dependencies low.
There are a few standard packages that must be installed
and one package `linetools` under review for
`astropy` affiliated status.

In general, we recommend that you use Anaconda for the majority of
these installations.

Detailed installation instructions are presented below:

Python Dependencies
-------------------

specdb depends on the following list of Python packages.

We recommend that you use `Anaconda <https://www.continuum.io/downloads/>`_
to install and/or update these packages.

* `python <http://www.python.org/>`_ versions 3.6or later
* `numpy <http://www.numpy.org/>`_ version 1.12 or later
* `astropy <http://www.astropy.org/>`_ version 1.3 or later
* `scipy <http://www.scipy.org/>`_ version 0.18 or later
* `matplotlib <http://matplotlib.org/>`_  version 1.4 or later

If you are using Anaconda, you can check the presence of these packages with::

	conda list "^python|numpy|astropy|scipy|matplotlib"

If the packages have been installed, this command should print
out all the packages and their version numbers.

If any of these packages are missing you can install them
with a command like::

	conda install astropy

If any of the packages are out of date, they can be updated
with a command like::

	conda update scipy

Installing rf_meta_query
========================

Presently, you must download the code from github::

	#go to the directory where you would like to install
	git clone https://github.com/realfastvla/rf_meta_query.git

From there, you can build and install with

	cd rf_meta_query
	python setup.py install  # or use develop


This should install the package and any scripts.
Make sure that your PATH includes the standard
location for Python scripts (e.g. ~/anaconda/bin)


