# SlackDataCollector
#
# Unit tests for Collector
#
# @version: alpha-0.0.1
# @author: Bassem Dghaidy

import datetime
import json
import os
import unittest

from slackcollector.collector import Collector


class TestCollector(unittest.TestCase):

    def setUp(self):
        # Get the configuration file from /src/
        self.config_file = 'config.example.yml'

        # Load it
        self.collector_inst = Collector()

    def test_load_config_file_success(self):
        """
        True when the configuration file is loaded properly
        and values are stored as member variables
        """
        outcome = self.collector_inst.load_config(self.config_file)
        self.assertTrue(outcome)
        self.assertTrue(self.collector_inst.data_dir)
        self.assertTrue(self.collector_inst.data_file_prefix)

    def test_load_config_file_failure(self):
        """
        Test a non existent configuration file
        """
        outcome = self.collector_inst.load_config('/boguspath')
        self.assertFalse(outcome)

    def test_anonymize_data_success(self):
        """
        Test whether the data anonymizer works by removing sensitive
        JSON objects
        """
        test_json_file = os.path.join(os.path.dirname(__file__),
                                      '_test_data/sensitive_json.json')

        # Load the file
        with open(test_json_file) as data_file:
            json_data = json.load(data_file)
        # Anonymize it
        clean_json_data = self.collector_inst.anonymize_data(json_data)
        sensitive_keys_set = set(['profile', 'real_name', 'name'])
        # Check for occurences
        for item in clean_json_data['members']:
            # If the intersection of the "sensitive_keys_set" and keys sets is
            # empty the we have cleared these keys and their values
            self.assertFalse(sensitive_keys_set.intersection(set(item.keys())))

    def test_get_today_date(self):
        """
        Build the formatted date for today and test its equality
        with what's returned from get_today_date()
        """
        today = datetime.datetime.now()
        formatted_date = '{}-{}-{}'.format(today.day, today.month, today.year)
        self.assertEquals(formatted_date, self.collector_inst.get_today_date())


if __name__ == '__main__':
    unittest.main()
