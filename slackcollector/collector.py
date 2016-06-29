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

import yaml
import os
import io
import json
import datetime
import sys
import slack
import slack.users


class Collector:
    """The main class of the script.

    This class contains the methods for querying the API and
    manipulating the data.
    """

    def load_config(self, config_file_path):
        """
        Parses the yaml configuration file and stores the data into
        member variables
        """
        config_file = os.path.join(os.path.dirname(__file__),
                                   '../config/' + config_file_path)
        config = yaml.safe_load(open(config_file))
        self.data_dir = config['storage']['data_dir']
        self.data_file_prefix = config['storage']['data_file_prefix']
        slack.api_token = config['secure']['slack_group_token']

    def collect_data(self):
        """Query the Slack API and retrieve user data."""
        self.print_out('Information Retrieval Began ...')
        self.user_list = slack.users.list()
        self.print_out('Data Retrieved')
        return self.user_list

    def write_data(self, data):
        """Write data to the file specified in the configuration."""
        if not data:
            self.print_out('No data was retrieved. Aborting now ...',
                           'FATAL')
            sys.exit(0)
        date_time = self.get_today_date()
        file_name = '{}-{}.json'.format(self.data_file_prefix,
                                        date_time)
        output_file = os.path.join(self.data_dir, file_name)
        self.print_out(
            'Attempting to write data to output file: {}'.format(output_file))
        self.make_dir(self.data_dir)
        with io.open(output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.user_list,
                               ensure_ascii=False,
                               indent=4,
                               separators=(',', ': ')))
            self.print_out('Job complete.')

    def anonymize_data(self, data):
        """Remove all personal and private data."""
        for item in data['members']:
            item.pop('profile', None)
            item.pop('real_name', None)
            item.pop('name', None)

        return data

    def get_today_date(self):
        """Return a formatted date: day-month-year."""
        today = datetime.datetime.now()
        return '{}-{}-{}'.format(today.day, today.month, today.year)

    def make_dir(self, directory):
        """Create directories if they do not already exist."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def print_out(self, message, type='INFO'):
        """Log events to stdout."""
        print('{}::: {}'.format(type, message))


if __name__ == "__main__":
    collector_inst = Collector()
    try:
        collector_inst.load_config('config.yml')
    except IOError:
        collector_inst.print_out('Configuration file does not exist. Make sure'
                                 ' the file "config/config.yml" exists and is '
                                 'configured correctly.', 'FATAL')
        sys.exit(1)
    except yaml.scanner.ScannerError:
        collector_inst.print_out('Corrupted configuration file - could not be '
                                 'parsed make sure "config.yml" is configured '
                                 'correctly.', 'FATAL')
        sys.exit(2)
    data = collector_inst.collect_data()
    data = collector_inst.anonymize_data(data)
    try:
        collector_inst.write_data(data)
    except IOError as e:
        e = sys.exc_info()[0]
        collector_inst.print_out(
            'Failed to write data.\n'
            'Error: {}'.format(e),
            'FATAL')
        sys.exit(3)
