#!/usr/bin/python
#
# SlackDataCollector
#
# Script that uses the Slack python SDK
# to authenticate to the MENA-Devs Slack Group
# and collect relevant user information for the purpose
# of data analysis
#
# @version: alpha-0.0.1
# @author: Bassem Dghaidy

import yaml
import os
import io
import json
import datetime
import sys
import slack
import slack.users

class Collector:

    def load_config(self, config_file_path):
        """
        Parses the yaml configuration file and stores the data into
        member variables
        """
        # Load configuration file
        config_file = os.path.join(os.path.dirname(__file__), '../config/' + config_file_path)

        if not os.path.isfile(config_file):
            self.print_out('Configuration file does not exist. Make sure the '
                           'file "config/config.yml" exists and is configured '
                           'correctly.', 'FATAL')
            return False

        # Load the file
        config = yaml.safe_load(open(config_file))

        if not config:
            self.print_out('Corrupted configuration file - could not be '
                           'parsed make sure "config.yml" is configured '
                           'correctly.', 'FATAL')
            return False

        self.data_dir = config['storage']['data_dir']
        self.data_file_prefix = config['storage']['data_file_prefix']
        # Set the slack API token
        slack.api_token = config['secure']['slack_group_token']
        # All went well
        return True

    def collect_data(self):
        """
        Main method - it taps into the Slack SDK to retrieve the user list
        in json format then it passes this information to write_data()
        """
        self.print_out('Information Retrieval Began ...')
        # Attempt to retrieve the user list
        try:
            self.user_list = slack.users.list()
            self.print_out('Data Retrieved')
        except:
            # Exit if an exception was raised
            e = sys.exc_info()[0]
            self.print_out(
                'Failed to retrieve information from Slack: {}'.format(e),
                'FATAL')
            return False
        # Return the users list
        return self.user_list

    def write_data(self, data):
        """
        Write data to the file specified in the configuration
        """
        if not data:
            self.print_out('No data was retrieved. Aborting now ...',
                           'FATAL')
            sys.exit(0)
        # Setup the json file name
        date_time = self.get_today_date()
        file_name = '{}-{}.json'.format(self.data_file_prefix,
                                        date_time)
        output_file = os.path.join(self.data_dir, file_name)

        # Info message
        self.print_out(
            'Attempting to write data to output file: {}'.format(output_file))
        # Create the directory if it doesn't exist already

        self.make_dir(self.data_dir)
        # Write data to file
        with io.open(output_file, 'w', encoding='utf-8') as f:
            try:
                f.write(json.dumps(self.user_list,
                                   ensure_ascii=False,
                                   indent=4,
                                   separators=(',', ': ')))
            except:
                e = sys.exc_info()[0]
                self.print_out(
                    'Failed to write data into: {}\n'
                    'Error: {}'.format(output_file, e),
                    'FATAL')
                return False

            self.print_out('Job complete.')
            return True

    def anonymize_data(self, data):
        """
        Remove all personal and private data
        """
        if not data:
            return False

        for item in data['members']:
            # Remove user profile
            item.pop('profile', None)
            # Remove real name
            item.pop('real_name', None)
            # Remove name
            item.pop('name', None)

        return data

    def get_today_date(self):
        """
        Returns a formatted date: day-month-year
        """
        today = datetime.datetime.now()
        return '{}-{}-{}'.format(today.day, today.month, today.year)

    def make_dir(self, directory):
        """
        Create directories if they do not already exist
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    def print_out(self, message, type='INFO'):
        """
        Custom output
        """
        print('{}::: {}'.format(type, message))


if __name__ == "__main__":
    # Create a new Collector instance
    # and pass the configuration as a param
    collector_inst = Collector()

    # Try to load the configuration file
    if collector_inst.load_config('config.yml'):
        # Initiate the collection process
        data = collector_inst.collect_data()
        # Write data into the file
        data = collector_inst.anonymize_data(data)
        # Write clean data into file
        collector_inst.write_data(data)
