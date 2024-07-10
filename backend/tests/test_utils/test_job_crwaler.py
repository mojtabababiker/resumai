import os
import unittest
from unittest.mock import MagicMock, _patch_dict, patch
from urllib.parse import urlencode
import requests
from utils.job_crawler import JobCrawler

class TestJobCrawler(unittest.TestCase):
    """Test the JobCrawler class utility"""

    @classmethod
    def setUpClass(cls):
        """Setup the test environment"""
        os.environ['SCRAP_PROXY_API_KEY'] = 'mocked_api_key'
        os.environ['SCARP_PROXY_URL'] = 'https://mocked_url.com'
        cls.mocked_markdownify = patch('utils.job_crawler.md').start()
        cls.mocked_markdownify.return_value = "This is the job description in markdown format"


    def setUp(self):
        self.crawler = JobCrawler()

    def test_get_description_valid_url(self):
        url = "https://www.linkedin.com/jobs/view/3960296277"
        expected_description = "This is the job description in markdown format"
        
        # Mocking the requests.get method to return a response with the expected description
        with patch('requests.get') as mock_get:
            mocked_response = MagicMock()
            mocked_response.raise_for_status.return_value = None
            mocked_response.text = '''
            <body>
                <div class="decorated-job-posting__details">
                    <!---->
                    <section class="core-section-container my-3 description">
                        <!---->
                        <!---->
                        <!---->
                        <div class="core-section-container__content break-words">
                        <!---->
                        <div class="description__text description__text--rich">
                            <section class="show-more-less-html show-more-less-html--more" data-max-lines="5">
                            <div class="show-more-less-html__markup relative overflow-hidden">
                                <p><strong>Role Description</strong></p>
                                <p>This is a full-time hybrid role for a Python Backend Developer located in 6th of October, with flexibility for some remote work. The Senior Python Backend Developer will be responsible for the day-to-day tasks associated with designing and implementing back-end solutions, including programming, software development, and object-oriented programming (OOP). The Senior Python Backend Developer will also collaborate with cross-functional teams and troubleshoot issues as they arise.</p>
                                <p><strong>Qualifications</strong></p>
                                <ul>
                                <li>Strong Computer Science skills</li>
                                <li>Extensive experience in Back-End Web Development</li>
                                <li>Proficiency in Python</li>
                                <li>Experience in Software Development and Programming</li>
                                <li>Experience in Object-Oriented Programming (OOP)</li>
                                <li>Excellent problem-solving and troubleshooting skills</li>
                                <li>Ability to work collaboratively with cross-functional teams</li>
                                <li>Strong communication and interpersonal skills</li>
                                <li>Bachelor's or Master's degree in Computer Science or a related field</li>
                                </ul>
                            </div>
                            <button class="show-more-less-html__button show-more-less-button
                                show-more-less-html__button--more
                                ml-0.5" data-tracking-control-name="public_jobs_show-more-html-btn" aria-label="i18n_show_more" aria-expanded="false">
                                <!---->
                                Show more
                                <icon class="show-more-less-html__button-icon show-more-less-button-icon lazy-loaded" aria-hidden="true" aria-busy="false">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" preserveAspectRatio="xMinYMin meet" focusable="false" class="lazy-loaded" aria-busy="false">
                                    <path d="M8 9l5.93-4L15 6.54l-6.15 4.2a1.5 1.5 0 01-1.69 0L1 6.54 2.07 5z" fill="currentColor"></path>
                                </svg>
                                </icon>
                            </button>
                            <button class="show-more-less-html__button show-more-less-button
                                show-more-less-html__button--less
                                ml-0.5" data-tracking-control-name="public_jobs_show-less-html-btn" aria-label="i18n_show_less" aria-expanded="true">
                                <!---->
                                Show less
                                <icon class="show-more-less-html__button-icon show-more-less-button-icon lazy-loaded" aria-hidden="true" aria-busy="false">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" preserveAspectRatio="xMinYMin meet" focusable="false" class="lazy-loaded" aria-busy="false">
                                    <path d="M8 7l-5.9 4L1 9.5l6.2-4.2c.5-.3 1.2-.3 1.7 0L15 9.5 13.9 11 8 7z" fill="currentColor"></path>
                                </svg>
                                </icon>
                            </button>
                            <!---->    
                            </section>
                        </div>
                        <ul class="description__job-criteria-list">
                            <!---->      
                            <li class="description__job-criteria-item">
                            <h3 class="description__job-criteria-subheader">
                                Employment type
                            </h3>
                            <span class="description__job-criteria-text description__job-criteria-text--criteria">
                            Full-time
                            </span>
                            </li>
                            <!----><!---->    
                        </ul>
                        </div>
                    </section>
                    <section class="core-section-container my-3 find-a-referral">
                        <!---->
                        <!---->
                        <!---->
                        <div class="core-section-container__content break-words">
                        <div class="face-pile flex !no-underline">
                            <div class="face-pile__images-container self-start flex-shrink-0 mr-1 leading-[1]">
                            <img class="inline-block relative rounded-[50%] w-4 h-4 face-pile__image border-1 border-solid border-color-transparent -ml-2 first:ml-0 lazy-loaded" data-ghost-classes="bg-color-entity-ghost-background" data-ghost-url="https://static.licdn.com/aero-v1/sc/h/9c8pery4andzj6ohjkjp54ma2" alt="" aria-busy="false" src="https://static.licdn.com/aero-v1/sc/h/ed3f1qhk2nzarhqpe785yhr1j">
                            <img class="inline-block relative rounded-[50%] w-4 h-4 face-pile__image border-1 border-solid border-color-transparent -ml-2 first:ml-0 lazy-loaded" data-ghost-classes="bg-color-entity-ghost-background" data-ghost-url="https://static.licdn.com/aero-v1/sc/h/9c8pery4andzj6ohjkjp54ma2" alt="" aria-busy="false" src="https://static.licdn.com/aero-v1/sc/h/boxt1zgrwnv3ss0ch8fpldqox">
                            <img class="inline-block relative rounded-[50%] w-4 h-4 face-pile__image border-1 border-solid border-color-transparent -ml-2 first:ml-0 lazy-loaded" data-ghost-classes="bg-color-entity-ghost-background" data-ghost-url="https://static.licdn.com/aero-v1/sc/h/9c8pery4andzj6ohjkjp54ma2" alt="" aria-busy="false" src="https://static.licdn.com/aero-v1/sc/h/6fw6jn9040cngf2toi2pvzkn6">
                            </div>
                            <div class="find-a-referral__cta-container">
                            <p>Referrals increase your chances of interviewing at Tawasolmap by 2x</p>
                            <a class="find-a-referral__cta" href="https://www.linkedin.com/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fsearch%2Fresults%2Fpeople%2F%3FfacetCurrentCompany%3D35576778&amp;emailAddress=&amp;fromSignIn=&amp;trk=public_jobs_find-a-referral-cta" data-tracking-control-name="public_jobs_find-a-referral-cta" data-tracking-will-navigate="">
                            See who you know
                            </a>
                            </div>
                        </div>
                        </div>
                    </section>
                    <!---->    
                </div>
            </body>
            '''
            mock_get.return_value = mocked_response
            
            description = self.crawler.get_description(url)
            mock_get.assert_called_once_with(os.environ['SCARP_PROXY_URL'], params=urlencode({'api_key': os.environ['SCRAP_PROXY_API_KEY'] , 'url': url}), timeout=35)
            self.assertEqual('linkedin', self.crawler.platform)
            self.mocked_markdownify.assert_called_once()
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