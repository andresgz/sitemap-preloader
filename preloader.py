import requests, validators
from bs4 import BeautifulSoup


class Preloader:
    """
    Preloader class to fetch all URLs from a sitemap and its sitemap index"""

    def __init__(self, sitemap_url, depth=2):
        """
        :param sitemap_url: URL of the sitemap
        :param depth: Depth of the sitemap index
        """
        self.sitemap_url = sitemap_url
        self.sitemap_urls = set()
        self.page_urls = set()
        self.failed_urls = {}
        self.finished_pages = []
        self.original_pages = set()
        if depth < 1:
            raise ValueError("depth must be greater than 1")
        self.depth = depth
        self.extract_urls()

    def extract_urls(self):
        """
        Extracts all URLs from the sitemap and store them in a set
        """
        self.fetch_url(self.sitemap_url)
        print(f"Found {len(self.sitemap_urls)} sitemaps")
        print(f"Found {len(self.page_urls)} pages")
        self.original_pages = self.page_urls.copy()

    def fetch_pages(self, batch_size=None):
        """
        Fetches extracted urls
        """
        total_pages = len(self.page_urls)
        fetched_pages = 0

        print(
            f"Will process {batch_size if batch_size else total_pages} pages of {total_pages}"
        )

        page_urls = list(self.page_urls)
        pages_range = page_urls[:batch_size] if batch_size else page_urls
        for url in pages_range:
            fetched_pages += 1
            print(
                f"Fetching page: {fetched_pages}/{batch_size if batch_size else total_pages}"
            )
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
                self.finished_pages.append(sitemap_url)
                self.page_urls.remove(sitemap_url)

        else:
            print(f"Failed to fetch URL: {response.status_code}")
            if response.status_code in self.failed_urls:
                self.failed_urls[response.status_code].append(sitemap_url)
            else:
                self.failed_urls[response.status_code] = [sitemap_url]

            if level == self.depth:
                self.page_urls.remove(sitemap_url)
            else:
                self.sitemap_urls.remove(sitemap_url)

    def add_url(self, base_set, url):
        """
        Adds a URL to the provided set if it's valid only
        :param base_set: Set to add the URL to
        :param url: URL to add to the set
        """
        if validators.url(url):
            base_set.add(url)
