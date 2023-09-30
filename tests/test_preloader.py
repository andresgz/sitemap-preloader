import sys
import os

# Add the project's root directory to the Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import pytest, requests
from preloader import Preloader
from unittest.mock import patch, Mock

# Define the path to the external mock XML file
MOCK_XML_FILE_MAIN = os.path.join(os.path.dirname(__file__), "mock_sitemap_main.xml")
MOCK_XML_FILE_SUB1 = os.path.join(os.path.dirname(__file__), "mock_sitemap_sub1.xml")
MOCK_XML_FILE_SUB2 = os.path.join(os.path.dirname(__file__), "mock_sitemap_sub2.xml")
MOCK_PAGE = os.path.join(os.path.dirname(__file__), "page.html")


@pytest.fixture
def mock_requests_get():
    def custom_get(url, *args, **kwargs):
        response = requests.Response()
        if url == "https://example.com/sitemap.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_MAIN, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_sub1.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_SUB1, "rb") as mock_file:
                response._content = mock_file.read()
        elif url == "https://example.com/sitemap_sub2.xml":
            response.status_code = 200
            with open(MOCK_XML_FILE_SUB2, "rb") as mock_file:
                response._content = mock_file.read()
        elif (
            url == "https://example.com/page1.html"
            or url == "https://example.com/page2.html"
            or url == "https://example.com/page3.html"
            or url == "https://example.com/page4.html"
            or url == "https://example.com/page5.html"
            or url == "https://example.com/page6.html"
        ):
            response.status_code = 200
            with open(MOCK_PAGE, "rb") as mock_file:
                response._content = mock_file.read()
        else:
            response.status_code = 404
        return response

    with patch("requests.get", side_effect=custom_get) as mock_get:
        yield mock_get


def test_mock_ok(mock_requests_get):
    response = requests.get("https://example.com/sitemap.xml")
    assert response.status_code == 200
    with open(MOCK_XML_FILE_MAIN, "rb") as file:
        expected_content = file.read()
    assert response.content == expected_content


def test_mock_fail(mock_requests_get):
    response = requests.get("https://example.com/other.xml")
    assert response.status_code == 404


def test_preloader_fetch_level_1(mock_requests_get):
    preloader = Preloader("https://example.com/sitemap.xml", depth=1)
    assert len(preloader.page_urls) == 2
    assert len(preloader.sitemap_urls) == 0

def test_preloader_level_2(mock_requests_get):
    preloader = Preloader("https://example.com/sitemap.xml", depth=2)
    assert preloader.sitemap_url == "https://example.com/sitemap.xml"
    assert len(preloader.page_urls) == 6
    assert len(preloader.sitemap_urls) == 2

def test_preloader_level_3(mock_requests_get):
    preloader = Preloader("https://example.com/sitemap.xml", depth=3)
    assert preloader.sitemap_url == "https://example.com/sitemap.xml"
    assert len(preloader.page_urls) == 0
    assert len(preloader.sitemap_urls) == 8

if __name__ == "__main__":
    pytest.main()
