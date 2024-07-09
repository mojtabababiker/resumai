import unittest
from unittest.mock import patch
import requests
from utils.job_crawler import JobCrawler

class TestJobCrawler(unittest.TestCase):
    """Test the JobCrawler class utility"""

    @classmethod
    def setUpClass(cls):
        """Setup the test environment"""
        cls.mocked_getenv = patch('os.getenv')
        cls.mocked_getenv['SCRAP_PROXY_API_KEY'] = 'mocked_api_key'
        cls.mocked_getenv['SCRAP_PROXY_URL'] = 'mocked_url'
        cls.mocked_getenv.start()

    def setUp(self):
        self.crawler = JobCrawler()

    def test_get_description_valid_url(self):
        url = "https://www.linkedin.com/jobs/view/3960296277"
        expected_description = "This is the job description in markdown format"
        
        # Mocking the requests.get method to return a response with the expected description
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "<body>This is the job description</body>"
            description = self.crawler.get_description(url)
            mock_get.assert_called_once_with()
            self.assertEqual(description, expected_description)

    def test_get_description_invalid_url(self):
        url = "https://www.invalidurl.com"
        
        # Mocking the requests.get method to raise an exception
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.InvalidURL  #type: ignore
            with self.assertRaises(ValueError):
                self.crawler.get_description(url)

    def test_get_description_no_description_found(self):
        url = "https://www.linkedin.com/jobs/view/1234567890"
        
        # Mocking the requests.get method to return a response without a job description
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "<body></body>"
            with self.assertRaises(ValueError):
                self.crawler.get_description(url)

if __name__ == '__main__':
    unittest.main()