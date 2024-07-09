#!/usr/bin/env python3
"""A utitlty helper to crawl job descriptions"""
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from markdownify import markdownify as md


load_dotenv('.env', verbose=True)


class JobCrawler:
    def __init__(self) -> None:
        """Construct a JobCrawler object with the needed attributes"""
        self.__proxy_url = os.getenv('SCARP_PROXY_URL')
        self.__proxy_params = {
            'api_key': os.getenv('SCRAP_PROXY_API_KEY'),
            'url': '',
        }
        self._platforms_tags = {
            'linkedin': [
                {'tag': 'div', 'class': 'decorated-job-posting__details'},
                {'tag': 'section', 'class': 'description'},
                {'tag': 'section', 'class': 'show-more-less-html'},
                {'tag': 'div', 'class': 'show-more-less-html__markup'},
                ],
        }
        self._parse_tags = None
        self.platform = None

    def get_description(self, url: str) -> str:
        """The main interface of the JobCrawler class, get the job description from the given url
        and return it as markdown

        Parameters:
        -----------
        * url (str): the url of the job

        Returns:
        --------
        * str: the job description in markdown format
        """
        #TODO:
        # *1. add redis caching to avoid multiple requests to the same url, based on the url as key and the description as value

        self.platform = self._get_paltform_from_url(url)
        if not self.platform:
            raise ValueError("Platform not supported")
        
        self.__proxy_params['url'] = url
        try:
            response = requests.get(self.__proxy_url, params=urlencode(self.__proxy_params), timeout=35)
            response.raise_for_status()
        except requests.exceptions.InvalidURL:
            raise ValueError("Invalid URL")
        except requests.exceptions.ConnectionError:
            raise ValueError("Connection Error")
        except requests.exceptions.HTTPError as e:
            raise ValueError("Not Found")
        
        self._parse_tags = self._platforms_tags.get(self.platform)

        page_text = self._parse_html(response.text)

        job_description = self._to_markdown(page_text)
        if not job_description:
            raise ChildProcessError("Failed to convert the job description to markdown")
        # add the result to the cache
        return job_description

    def _get_paltform_from_url(self, url: str) -> str | None:
        """Get the platform name from the url
        
        Parameters:
        -----------
        * url (str): the url of the job
        
        Returns:
        --------
        * str: the platform name, None if not found
        """
        if "linkedin" in url:  # TODO: seek better way to identify the platform
            return "linkedin"
        return None

    def _parse_html(self, html: str) -> str|None:
        """Parse the html page of the job and return the description

        Parameters:
        -----------
        * html (str): the html page of the job

        Returns:
        --------
        * str: the job description, raises ValueError if no description found
        """
        soup = BeautifulSoup(html, "html.parser")
        description = soup.find("body")
        for tag in self._parse_tags:  # type: ignore
            description = description.find(tag.get("tag"), class_=tag.get("class"))  # type: ignore

        if not description:
            raise ValueError("No job description found")

        return str(description)
    
    def _to_markdown(self, html: str) -> str:
        """Convert the job description html to markdown format

        Parameters:
        -----------
        * html (str): the job description html

        Returns:
        --------
        * str: the job description in markdown format
        """
        return md(html, heading_style="ATX", bullet_style=["*", "-"], strip=["script", "style", "a"])
    
if __name__ == '__main__':
    crawler = JobCrawler()
    url = "https://www.linkedin.com/jobs/view/3960296277"
    print(crawler.get_description(url))