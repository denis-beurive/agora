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

## Dev and tests

For test (load only 200 rows per CSV file):

    python -m agora.agora --verbose --test ./data ./output

Skip the generation of monthly documents:

    python -m agora.agora --verbose --skip-monthly ./data ./output

Skip the generation of _some documents_ (the ones that take very long time to generate) if they already exist:

    python -m agora.agora --verbose --skip-if-exists ./data ./output

# Running the unit tests
    
    python run_unittest.py --verbose

# Documents

* [transactions per vendors](output/vendor/transactions.md)
* [transactions per shipping locality](output/ship-from/transactions.md)
* [total amount of transactions per month](output/transaction/total-transactions.md)
* [total number of transactions per month](output/transaction/total-transactions.md)

