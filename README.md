# Description

A deep dive into the dark WEB.

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
    
# Running the unit tests
    
    python run_unittest.py --verbose

# Generate the wheel

    python setup.py sdist

# Install the wheel

There are two ways to install the wheel:

* you can install the wheel with the default features.
* you can install the wheel with extra features.

> Please note that there is no way to install a wheel in _editable/developer_ mode.
> The package (inside the wheel) will be installed as a dependency of your project (under a directory which path is
> given by the command `pipenv --venv`).

## Install the wheel with the default features

    pipenv install /path/to/dist/my_project-0.1.tar.gz

Test:

    python -c "import my_package.my_module"    
    hello

## Install the wheel with an extra feature (dev)

    pipenv install --find-links=/path/to/dist/my_project-0.1.tar.gz "my_project [dev]"

> Please note that, in our example, the extra feature called `dev` **has nothing to do with the _editable/developer_
> mode**.
> Edit the file `setup.py` and look at the following parameter: `extras_require={'dev': requirements_dev}`.
> An _extra feature_ only specifies the installation of extra packages.

## Get information about the installation

### Dependencies folder

If you wonder where the package has been installed, then you can execute the command below.

    pipenv --venv

### Get the list of installed dependencies

    $ pipenv run pip list
    Package           Version   Location
    ----------------- --------- --------------------------------------
    agora             0.1       /home/denis/Documents/github/agora/src
    astroid           2.5.7
    certifi           2020.12.5
    chardet           4.0.0
    idna              2.10
    isort             5.8.0
    lazy-object-proxy 1.6.0
    mccabe            0.6.1
    panda             0.3.1
    pip               20.1.1
    pkg-resources     0.0.0
    pylint            2.8.2
    requests          2.25.1
    setuptools        44.0.0
    toml              0.10.2
    urllib3           1.26.5
    wheel             0.36.2
    wrapt             1.12.1
    xmlrunner         1.7.7

Where does the name "`aroga`" come from ?

Short response: it comes from the file `setup.py`.

Long response: edit the code `setup.py`. You can see the code given below:

    setuptools.setup(
        ...
        name="agora",
        ...
    )

> You should avoid the use of the character "_" within the value of the parameter "name".
> Although you could use the name "my_project", it would be converted into "my-project".

### Get information about an installed dependency

    pipenv run pip show my-project

### Get the value of PYTHONPATH

    python -c "import sys; print(\"\n\".join([f\"{f}\" for f in sys.path]))"

# Running Pylint

    python -m pylint --rcfile=pylintrc src/

# Other commands

Uninstall a package:

    pipenv uninstall args

> **WARNING**: you must reinstall the current project after this action: `pipenv install --dev`.
> And you should regenerate the "requirements" files.

Install a package for DEV environment only:

    pipenv install --dev xmlrunner

> **WARNING**: you must reinstall the current project after this action: `pipenv install --dev`.
> And you should regenerate the "requirements" files.

Remove the virtual environment:

    pipenv --rm

Uninstall all packages:

    pipenv uninstall --all
    pipenv uninstall --all-dev

> **WARNING**: you must reinstall the current project after this action: `pipenv install --dev`.
> And you should regenerate the "requirements" files.

# Build the wheel

    pipenv lock --requirements > requirements.txt && pipenv lock --requirements --dev > requirements-dev.txt



