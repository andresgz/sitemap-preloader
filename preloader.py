import requests, validators
from bs4 import BeautifulSoup


class Preloader:
    """
    Preloader class to fetch all URLs from a sitemap and its sitemap index"""

    def __init__(self, sitemap_url, depth=2, page_start=1):
        """
        :param sitemap_url: URL of the sitemap
        :param depth: Depth of the sitemap index
        """
        self.sitemap_url = sitemap_url
        self.sitemap_urls = set()
        self.page_urls = set()
        self.failed_urls = set()
        if page_start < 1:
            raise ValueError("page_start must be greater than 1")
        self.page_start = page_start
        if depth < 1:
            raise ValueError("depth must be greater than 1")
        self.depth = depth
        self.fetch()

    def fetch(self):
        """
        Fetches all URLs from the sitemap and its sitemap index
        """
        self.fetch_url(self.sitemap_url)
        print(f"Found {len(self.sitemap_urls)} sitemaps")
        # Fetch pages from sitemaps
        self.fetch_all_pages()

    def fetch_all_pages(self):
        """
        Fetches all URLs from the sitemap index
        """
        total_pages = len(self.page_urls) - self.page_start
        count_pages = self.page_start
        print(f"Will process {total_pages} pages")
        page_urls = list(self.page_urls)
        for url in page_urls[self.page_start :]:
            print(f"Fetching page: {count_pages + 1}/{total_pages}")
            count_pages += 1
            self.fetch_url(url, self.depth)

    def fetch_url(self, sitemap_url, level=0):
        """
        Fetches all URLs from a sitemap or sitemap index
        :param sitemap_url: URL of the sitemap or sitemap index
        :param level: Level of the sitemap index
        """
        print(f"Fetching: {sitemap_url}")
        response = requests.get(sitemap_url)
        urls = []
        if response.status_code == 200:
            # Don't analyze it if It's the latest level
            if level < self.depth:
                soup = BeautifulSoup(response.text, "xml")  # Use lxml as the parser
                urls = [loc.text for loc in soup.find_all("loc")]

                if level < self.depth - 1:
                    for url in urls:
                        self.add_url(self.sitemap_urls, url)
                        self.fetch_url(url, 1)
                elif level == self.depth - 1:
                    for url in urls:
                        self.add_url(self.page_urls, url)

        else:
            print(f"Failed to fetch URL: {response.status_code}")

    def add_url(self, base_set, url):
        """
        Adds a URL to the provided set if it's valid only
        :param base_set: Set to add the URL to
        :param url: URL to add to the set
        """
        if validators.url(url):
            base_set.add(url)
