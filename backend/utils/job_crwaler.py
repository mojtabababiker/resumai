#!/usr/bin/env python3
"""A utitlty helper to crawl job descriptions"""
import requests
from bs4 import BeautifulSoup


class JobCrawler:
    def __init__(self) -> None:
        """Construct a JobCrawler object with the needed attributes"""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br,zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
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
        """Get the job description from the given url"""
        self.platform = self._get_paltform_from_url(url)
        if not self.platform:
            raise ValueError("Platform not supported")
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.InvalidURL:
            raise ValueError("Invalid URL")
        except requests.exceptions.ConnectionError:
            raise ValueError("Connection Error")
        except requests.exceptions.HTTPError as e:
            # raise ValueError("Not Found")
            print(e)
            print(response.text)
            return response.text
        
        self._parse_tags = self._platforms_tags.get(self.platform)

        page_text = self._parse_html(response.text)
        if not page_text:
            raise ValueError("No job description found")
        return page_text

    def _get_paltform_from_url(self, url: str) -> str | None:
        """Get the platform name from the url"""
        if "linkedin" in url:  # TODO: seek better way to identify the platform
            return "linkedin"
        return None

    def _parse_html(self, html: str) -> str|None:
        """Parse the html and return the job description"""
        soup = BeautifulSoup(html, "html.parser")
        description = soup.find("body")
        for tag in self._parse_tags:  # type: ignore
            description = description.find(tag.get("tag"), class_=tag.get("class"))  # type: ignore
        print(description)
        return description.text if description else None
    
if __name__ == '__main__':
    crawler = JobCrawler()
    url = "https://www.linkedin.com/jobs/view/3960296277"
    print(crawler.get_description(url))