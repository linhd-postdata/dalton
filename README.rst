========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/averell/badge/?style=flat
    :target: https://readthedocs.org/projects/averell
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/linhd-postdata/averell.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/linhd-postdata/averell

.. |codecov| image:: https://codecov.io/github/linhd-postdata/averell/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/linhd-postdata/averell

.. |landscape| image:: https://landscape.io/github/linhd-postdata/averell/master/landscape.svg?style=flat
    :target: https://landscape.io/github/linhd-postdata/averell/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/averell.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/averell

.. |wheel| image:: https://img.shields.io/pypi/wheel/averell.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/averell

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/averell.svg
    :alt: Supported versions
    :target: https://pypi.org/project/averell

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/averell.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/averell

.. |commits-since| image:: https://img.shields.io/github/commits-since/linhd-postdata/averell/0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/linhd-postdata/averell/compare/0.0.1...master



.. end-badges

Corpora downloader and reader for Spanish sources

* Free software: Apache Software License 2.0

Installation
============

::

    pip install averell

You can also install the in-development version with::

    pip install https://github.com/linhd-postdata/averell/archive/master.zip


Documentation
=============


https://averell.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
