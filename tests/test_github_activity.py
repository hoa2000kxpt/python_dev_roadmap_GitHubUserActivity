import unittest
from unittest import patch, MagicMock
import urllib.error
from github_activity import fetch_user_activity

class TestGithubActivity(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_fetch_user_activity(self, mock_urlopen):
        # Mock a valid response with recent activity
        mock_response = MagicMock()
        mock_response.read.return_value = b'[{"type": "PushEvent", "repo": {"name": "torvalds/linux"}, "payload": {"commits": [{"message": "Update"}]}}]'
        mock_urlopen.return_value = mock_response

        with patch('builtins.print') as mock_print:
            fetch_user_activity('torvalds')
            mock_print.assert_any_call('Pushed 1 commit(s) to torvalds/linux')

    @patch('urllib.request.urlopen')
    def test_valid_user_no_activity(self, mock_urlopen):
        # Mock a valid response with no recent activity
        mock_response = MagicMock()
        mock_response.read.return_value = b'[]'
        mock_urlopen.return_value = mock_response

        with patch('builtins.print') as mock_print:
            fetch_user_activity('inactive_user123')
            mock_print.assert_any_call('No recent activity found for this user.')

    @patch('urllib.request.urlopen', side_effect=urllib.error.HTTPError(url=None, code=404, msg="Not Found", hdrs=None, fp=None))
    def test_invalid_username(self, mock_urlopen):
        # Simulate an invalid username (404)
        with patch('builtins.print') as mock_print:
            fetch_user_activity("invalid_user_123_xyz")
            mock_print.assert_any_call("User not found. Please check the username and try again.")
