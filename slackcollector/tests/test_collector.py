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

import json
import os
import unittest

from slackcollector.collector import Collector


class TestCollector(unittest.TestCase):

    def setUp(self):
        self.config_file = 'config.example.yml'
        self.collector_inst = Collector(self.config_file)

    def test_load_config_file_success(self):
        self.collector_inst.load_config(self.config_file)
        self.assertIsNotNone(self.collector_inst.data_dir)
        self.assertIsNotNone(self.collector_inst.data_file_prefix)

    def test_load_config_file_failure(self):
        """
        Test a non existent configuration file
        """
        self.assertRaises(IOError, self.collector_inst.load_config,
                          '/boguspath')

    def test_anonymize_data_success(self):
        """
        Test whether the data anonymizer works by removing sensitive
        JSON objects
        """
        test_json_file = os.path.join(os.path.dirname(__file__),
                                      '_test_data/sensitive_json.json')
        with open(test_json_file) as data_file:
            json_data = json.load(data_file)
        clean_json_data = self.collector_inst.anonymize_data(json_data)
        sensitive_keys_set = set(['profile', 'real_name', 'name'])
        for item in clean_json_data['members']:
            # If the intersection of the "sensitive_keys_set" and keys sets is
            # empty the we have cleared these keys and their values
            self.assertFalse(sensitive_keys_set & set(item))


if __name__ == '__main__':
    unittest.main()
