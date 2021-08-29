# Description

A deep dive into the dark WEB.

# Installation

Click [here](doc/installation.md) to get a detailed installation procedure.

> Note: you may want to consult [these tips for data exploration](doc/tips.md).

# Usage

## Real use

Usage (from the **project root folder**):

    python -m agora.agora --verbose ./data ./output

> **Note**: make sure to initialise the Python environment first!
> 
> * `pipenv shell`
> * `pipenv install --dev`
> 
> Please read the [installation guide](doc/installation.md) and the [notes about wheels](doc/wheel-notes.md) if
> see errors.
> 
> You can delete all previously generated documents: `find ./output -name "*.svg" -exec rm {} \;`

## Results

Please click on [this link](report.md).

## Dev and tests

**Usage**:

```shell
$ python -m agora.agora --help
usage: agora.py [-h] [--verbose] [--debug] [--test] [--skip-monthly] [--skip-if-exists] [--km-only] input_path output_path

Agora stat builder

positional arguments:
  input_path        path to the input directory
  output_path       path to the output directory

optional arguments:
  -h, --help        show this help message and exit
  --verbose         activate the verbose mode
  --debug           activate the debug mode
  --test            activate the test mode
  --skip-monthly    skip the generation of monthly graphs
  --skip-if-exists  skip the generation a graph if ot already exists
  --km-only         only generate KMeans data
(agora-XPqCgF3T) denis@labo:~/Documents/github/agora
```

**Examples for tests**:

Load only 1000 rows per CSV file (make execution faster):

    python -m agora.agora --verbose --test ./data ./output

Skip the generation of monthly documents:

    python -m agora.agora --verbose --skip-monthly ./data ./output

Skip the generation of _some documents_ (the ones that take very long time to generate) if they already exist:

    python -m agora.agora --verbose --skip-if-exists ./data ./output
