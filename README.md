# Description

A deep dive into the dark WEB.

# Installation

Click [here](doc/installation.md) to get a detailed installation procedure.

# Usage

Usage (from the **project root folder**):

    python -m agora.agora --verbose ./data ./output

> **Note**: make sure to initialise the Python environment first! (`pipenv shell` followed by `pipenv install --dev`).
> Please read the [installation guide](doc/installation.md) and the [notes about wheels](doc/wheel-notes.md) if
> see errors.

# Running the unit tests
    
    python run_unittest.py --verbose

# Documents

* [transactions per vendors](output/vendor/transactions.md)
* [transactions per shipping locality](output/ship-from/transactions.md)
