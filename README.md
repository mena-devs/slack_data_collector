# Slack Data Collector

Uses the Slack API to collect anonymized information about the community

## Installation instructions

### OSX

#### Step 1

Make sure you have `Python` installed

`brew install python3`

#### Step 2

Install needed packages

`pip3 install nose`

`pip3 install tox`

#### Step 3

Move example configuration file, rename it and add Slack authentication token.

`mv samples/config.example.yml slackcollector/config.yml`

#### Step 4

`python setup.py develop`

#### Step 5

Run the tests

`nosetests`

#### Step 6

Run the script

`python slackcollector/collector.py`
