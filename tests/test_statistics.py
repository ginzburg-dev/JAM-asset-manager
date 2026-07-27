"""Contract tests for community-edition statistics placeholders."""

import unittest

from jam_asset_manager import statistics


class StatisticsTestCase(unittest.TestCase):
    def test_public_statistics_functions_fail_explicitly(self):
        calls = (
            (statistics.calculate_efficiency, ("start", "end", "json", [])),
            (statistics.compare_data, ({}, {}, "start", "end", "json", [])),
            (statistics.calculate_ai_prediction, ("start", "end", [])),
            (statistics.get_raw_statistics, ("start", "end", [])),
            (statistics.export_statistics_to_xml, ({}, "xml", [])),
        )
        for function, arguments in calls:
            with self.subTest(function=function.__name__):
                with self.assertRaisesRegex(NotImplementedError, "commercial edition"):
                    function(*arguments)


if __name__ == "__main__":
    unittest.main()
