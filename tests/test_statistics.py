"""Contract tests for community-edition statistics placeholders."""

import unittest

import jam_statistics


class StatisticsTestCase(unittest.TestCase):
    def test_public_statistics_functions_fail_explicitly(self):
        calls = (
            (jam_statistics.calculate_efficiency, ("start", "end", "json", [])),
            (jam_statistics.compare_data, ({}, {}, "start", "end", "json", [])),
            (jam_statistics.calculate_AI_prediction, ("start", "end", [])),
            (jam_statistics.get_raw_statistics, ("start", "end", [])),
            (jam_statistics.export_statistics_to_XML, ({}, "xml", [])),
        )
        for function, arguments in calls:
            with self.subTest(function=function.__name__):
                with self.assertRaisesRegex(NotImplementedError, "commercial edition"):
                    function(*arguments)


if __name__ == "__main__":
    unittest.main()
