import json
import unittest
import urllib.error
from unittest.mock import patch

import wikipedia_changes


class TestWikipediaChanges(unittest.TestCase):
    def test_build_api_url_encodes_title(self):
        url = wikipedia_changes.build_api_url("Ball State University")
        self.assertIn("titles=Ball%20State%20University", url)
        self.assertIn("rvlimit=30", url)
        self.assertIn("redirects=1", url)

    def test_parse_api_response_redirect(self):
        data = {
            "query": {
                "redirects": [{"from": "Ball State Univ", "to": "Ball State University"}],
                "pages": {
                    "390375": {
                        "pageid": 390375,
                        "ns": 0,
                        "title": "Ball State University",
                        "revisions": [
                            {"user": "InternetArchiveBot", "timestamp": "2023-09-23T17:28:39Z"},
                            {"user": "Melchior2006", "timestamp": "2023-09-22T06:40:10Z"},
                        ],
                    }
                },
            }
        }

        redirect_target, changes = wikipedia_changes.parse_api_response(data)
        self.assertEqual(redirect_target, "Ball State University")
        self.assertEqual(len(changes), 2)
        self.assertEqual(changes[0], ("2023-09-23T17:28:39Z", "InternetArchiveBot"))

    def test_parse_api_response_missing_page(self):
        data = {"query": {"pages": {"-1": {"ns": 0, "title": "NoSuchPage", "missing": ""}}}}
        with self.assertRaises(wikipedia_changes.PageNotFoundError):
            wikipedia_changes.parse_api_response(data)

    def test_format_functions(self):
        self.assertEqual(
            wikipedia_changes.format_redirect_message("Ball State University"),
            "Redirected to Ball State University",
        )
        self.assertEqual(
            wikipedia_changes.format_change_line("2023-09-23T17:28:39Z", "User123"),
            "2023-09-23T17:28:39Z User123",
        )

    @patch("wikipedia_changes.fetch_json")
    def test_main_success(self, mock_fetch_json):
        mock_fetch_json.return_value = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "ns": 0,
                        "title": "Ball State University",
                        "revisions": [
                            {"user": "EditorA", "timestamp": "2023-09-23T17:28:39Z"},
                        ],
                    }
                }
            }
        }
        result = wikipedia_changes.main(["wikipedia_changes.py", "Ball State University"])
        self.assertEqual(result, 0)

    @patch("wikipedia_changes.fetch_json")
    def test_main_network_error(self, mock_fetch_json):
        mock_fetch_json.side_effect = urllib.error.URLError("timeout")
        result = wikipedia_changes.main(["wikipedia_changes.py", "Ball State University"])
        self.assertEqual(result, 3)

    def test_main_missing_argument(self):
        result = wikipedia_changes.main(["wikipedia_changes.py"])
        self.assertEqual(result, 1)

    @patch("wikipedia_changes.fetch_json")
    def test_main_missing_page(self, mock_fetch_json):
        mock_fetch_json.return_value = {"query": {"pages": {"-1": {"ns": 0, "title": "NoSuchPage", "missing": ""}}}}
        result = wikipedia_changes.main(["wikipedia_changes.py", "NoSuchPage"])
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
