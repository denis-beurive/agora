# Installation

This document describes that installation process.

# Preparation

If necessary, install `pipenv`:

    sudo apt install pipenv

# Setup a virtual environment

    pipenv install --three
    pipenv shell

Install the distribution in _editable/developer_ mode:

    pipenv install --dev

> Please note that the command (`pipenv install --dev`) above will execute the script `setup.py`.
> The script `setup.py` needs the files `requirements.txt` and `requirements-dev.txt`.
> However, keep in mind that during the actual command execution, **the contents of these files are not used** - since
> the requirements are listed into the file `Pipfile` (see the sections `[dev-packages]` and `[packages]`).
>
> Edit the file `Pipfile` and look at the sections `[dev-packages]` and `[packages]`.
> * `[dev-packages]`: defines the dependencies for development.
>   Pay attention to this line: `my-project = {editable = true,path = "."}`.
>   This line specifies that the package must be installed in _editable/developer_ mode.
>   "`my-project`" is the value of the parameter `name` (within the function call `setuptools.setup()` - see file
>   `setup.py`).
>   It appears in the output of the command `pipenv run pip list`.
> * `[packages]`: defines the dependencies for nominal use.
>
> In case you need to re-generate the _requirements files_ (used by `setup.py`):
>
> `pipenv lock --requirements --dev > requirements-dev.txt`
> `pipenv lock --requirements > requirements.txt`

Test that the environment is well configured. The package `xmlrunner` should be installed and `PYTHONPATH` should point
to the directory `./src`.

    python -c "import xmlrunner"
    python -c "import sys; print(\"\n\".join([f\"{f}\" for f in sys.path]))"

At this point you should be OK.

# Extra notes

If you have troubles, please read these [notes about wheels](wheel-notes.md).
