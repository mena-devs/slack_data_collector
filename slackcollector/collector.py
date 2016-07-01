#!/usr/bin/python
#
# The MIT License (MIT)

# Copyright (c) 2016 Mena-Devs

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""The main Collector module."""

import yaml
import os
import io
import json
import datetime
import sys
import slack
import slack.users
import logging


class Collector:
    """The main class of the script.

    This class contains the methods for querying the API and
    manipulating the data.
    """

    def __init__(self, config_file=None):
        """Load the config file and handle potential errors."""
        self.configure_logging()
        try:
            self.load_config(config_file)
        except IOError:
            self.logger.error(
                'Configuration file does not exist. Make sure'
                ' the file "{}" exists and is '
                'configured correctly.'.format(config_file))
            sys.exit(1)
        except yaml.scanner.ScannerError:
            self.logger.error(
                'Corrupted configuration file - could not be '
                'parsed make sure "{}" is configured '
                'correctly.'.format(config_file))
            sys.exit(2)

    def configure_logging(self, level=logging.DEBUG):
        """Instanciate and configure a logger."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def load_config(self, config_file_path):
        """Parse the configuration file."""
        config_file = os.path.join(os.path.dirname(__file__),
                                   '../config/' + config_file_path)
        config = yaml.safe_load(open(config_file))
        self.data_dir = config['storage']['data_dir']
        self.data_file_prefix = config['storage']['data_file_prefix']
        slack.api_token = config['secure']['slack_group_token']

    def collect_data(self):
        """Query the Slack API and retrieve user data."""
        self.logger.info('Retrieving user list')
        self.user_list = slack.users.list()
        self.logger.info('User list retrieved')
        return self.user_list

    def write_data(self, data):
        """Write data to the file specified in the configuration."""
        date_time = datetime.datetime.now().strftime('%d-%M-%Y')
        file_name = '{}-{}.json'.format(self.data_file_prefix,
                                        date_time)
        output_file = os.path.join(self.data_dir, file_name)
        self.logger.info('Writing data to output file: {}'.format(output_file))
        try:
            os.makedirs(self.data_dir)
        except OSError:
            # The directory exists already
            pass
        with io.open(output_file, 'w', encoding='utf-8') as f:
            try:
                f.write(json.dumps(self.user_list,
                                   ensure_ascii=False,
                                   indent=4,
                                   separators=(',', ': ')))
                self.logger.info('Writing complete')
            except IOError as e:
                e = sys.exc_info()[0]
                collector.logger.error(
                    'Failed to write data.\n'
                    'Error: {}'.format(e))
                sys.exit(3)

    def anonymize_data(self, data):
        """Remove all personal and private data."""
        for item in data['members']:
            item.pop('profile', None)
            item.pop('real_name', None)
            item.pop('name', None)

        return data


if __name__ == "__main__":
    collector = Collector('config.yml')
    data = collector.collect_data()
    data = collector.anonymize_data(data)
    collector.write_data(data)
