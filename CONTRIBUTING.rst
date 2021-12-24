Contributing
============

Development requirements
------------------------

- ``poetry`` installed
- The required Python versions (see ``tox.ini``) installed.

Suggested setup on MacOS
^^^^^^^^^^^^^^^^^^^^^^^^

Installing the Python version is easy with ``pyenv`` and ``pyenv-virtualenv``.

.. code-block:: bash

   # be sure to follow installation instructions and documentation
   brew install pyenv pyenv-virtualenv

   # if using pyenv-virtualenv, remember to disable poetry virtualenvs
   poetry config virtualenvs.create false

   pyenv install -v [the required python versions]
   pyenv virtualenv [the main python version, e.g. 3.9.x] quacks
   # navigate to the repo root
   pyenv local quacks [all required python versions separated by space]
   # virtualenv and python versions now accessible when in this directory :)

Running the tests
-----------------

You can rull all checks locally with ``tox``:

.. code-block:: bash

   # run all checks
   tox
   # run all checks in parallel
   tox -p auto
   # run particular checks
   tox -e mypy
   tox -e py310
   tox -e docs,py39,mypy

Of course, you can also run ``pytest`` for a quick check.

Submitting a PR
---------------

When submitting a PR, be sure to follow the provided checklist. Thanks!
