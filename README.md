# Slack Data Collector

    version: alpha-0.0.1

| Branch | Build Status |
| ------ | --- |
| master | [![Build Status](https://travis-ci.org/mena-devs/slack_data_collector.svg?branch=master)](https://travis-ci.org/mena-devs/slack_data_collector) |
| alpha-0.0.2 | [![Build Status](https://travis-ci.org/mena-devs/slack_data_collector.svg?branch=alpha-0.0.2)](https://travis-ci.org/mena-devs/slack_data_collector) |

### Synopsis

Uses the Slack API to collect anonymized information about the community

### Installation & Configuration

#### Minimum Requirements

  ```
  - Python 2.7 or 3.5
  - pip or pip3

  # For testing
  - tox
  - nose
  ```

1. Clone the repository into any directory you have access to:

    ```sh
    git clone https://github.com/mena-devs/slack_data_collector
    ```

2. Copy the example configuration file, rename it `config.yml` and modify it to your liking:

    ```sh
    cp config/config.example.yml config/config.yml
    ```

3. Install the package:

    ```sh
    python setup.py develop
    ```

4. Run the tests (skip this step if you haven't installed nose)

    ```sh
    nosetests
    ```

5. Run the script

    ```sh
    python slackcollector/collector.py
    ```

### Unit Testing

To run the unit tests, you need to install `nose` and `tox` packages:

```sh
pip install nose
pip install tox
```

Run the tests:

```sh
# Run unit tests only
nosetests

# Test against python 2.7 and 3.5 and run the linters
tox
```

### Sample Output

```json
{
    "cache_ts": 1466800744,
    "members": [
        {
            "presence": "away",
            "deleted": true,
            "id": "U04B7LSFG",
            "is_bot": true,
            "team_id": "T03B400RJ"
        },
        {
            "presence": "away",
            "is_ultra_restricted": false,
            "deleted": false,
            "is_owner": false,
            "tz_label": null,
            "is_admin": false,
            "is_restricted": false,
            "is_primary_owner": false,
            "id": "U0AE305C4",
            "tz": "EET",
            "color": "50a0cf",
            "tz_offset": 10800,
            "has_2fa": false,
            "team_id": "T03B400RJ",
            "is_bot": false,
            "status": null
        },
        {
            "presence": "away",
            "is_ultra_restricted": false,
            "deleted": false,
            "is_owner": false,
            "tz_label": null,
            "is_admin": false,
            "is_restricted": false,
            "is_primary_owner": false,
            "id": "U03B5176N",
            "tz": "EET",
            "color": "e7392d",
            "tz_offset": 10800,
            "has_2fa": false,
            "team_id": "T03B400RJ",
            "is_bot": false,
            "status": null
        },
        {
            "presence": "away",
            "is_ultra_restricted": false,
            "deleted": false,
            "is_owner": false,
            "tz_label": null,
            "is_admin": false,
            "is_restricted": false,
            "is_primary_owner": false,
            "id": "U03CWMQSH",
            "tz": "EET",
            "color": "db3150",
            "tz_offset": 10800,
            "has_2fa": false,
            "team_id": "T03B400RJ",
            "is_bot": false,
            "status": null
        }
        ...
    ],
    "ok": true
}
```