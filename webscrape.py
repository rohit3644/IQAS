# importing third-party libraries

import urllib.parse as urlparse
from bs4.element import Comment
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import urllib.request
import requests
import spacy
import datetime

# Disable displaying SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# WebScraping class contains a constructor, get_random_ua function,
# get_random_delay function, google_search function, get_wiki_info function,
# get_all_wikis function, download_site function, download_all_sites function,
# filterTags function, text_from_html function, extract_text function
# and fetch_text_result function
class WebScraping:
    def __init__(self, query_array):
        self.query_array = query_array

    # Utility function to pick a random user-agent
    def get_random_ua(self):
        import numpy as np

        random_ua = None
        ua_file = 'ua_file.txt'
        try:
            ua_file_text = uploaded['ua_file.txt'].decode("utf-8")
            lines = ua_file_text.split('\n')
            # with open(ua_file) as f:
            # lines = f.readlines()
            if len(lines) > 0:
                prng = np.random.RandomState()
                index = prng.permutation(len(lines) - 1)
                idx = np.asarray(index, dtype=np.integer)[0]
                random_ua = lines[int(idx)]
        except Exception as ex:
            pass
        finally:
            return random_ua

    # Utility function to pick a random delay

    def get_random_delay(self):
        import numpy as np

        delay = 2.0
        try:
            random_num = np.random.uniform(2, 3)
            delay = round(random_num, 4)
        except Exception:
            pass
        finally:
            return delay

    # Get top sites from google for a query

    def google_search(self, query, num_results=None):
        from googlesearch import search

        def empty():  # Empty generator
            yield from ()
        results = empty()
        try:
            results = search(
                query, lang='en',
                start=0, stop=num_results,
                pause=self.get_random_delay(),
                user_agent=self.get_random_ua()
            )
        except Exception:
            pass
        finally:
            return results

    # Helper function to retrieve information directly from Wikipedia

    def get_wiki_info(self, wiki_url):
        import wikipedia
        import wikipediaapi
        import urllib.parse as urlparse
        wiki_text = ""
        url_segments = wiki_url.rpartition('/')
        if "en.wikipedia.org" == url_segments[2]:
            return wiki_text
        try:
            wikipedia.set_lang("en")
            wikipedia.set_rate_limiting(True,
                                        min_wait=datetime.timedelta(0, 0, 50000))

            title_path = url_segments[2]
            title = urlparse.unquote(title_path)
            title = title.replace("_", " ")
            wikiWiki = wikipediaapi.Wikipedia('en')
            wiki_page = wikiWiki.page(title)
            #contents += pagePy.summary
            #wiki_page = wikipedia.page(title)
            wiki_text = wiki_page.summary
        except (IndexError, wikipedia.exceptions.WikipediaException):
            pass
        finally:
            return wiki_text

    # Retrieve information from all wiki pages

    def get_all_wikis(self, wiki_links):
        wiki_contents = []
        for url in wiki_links:
            wiki_info = self.get_wiki_info(url)
            if wiki_info:
                wiki_contents.append(wiki_info)
        return wiki_contents

    # Helper function to download the html page of a site

    def download_site(self, url, session):
        html_page = ""
        user_agent = self.get_random_ua()
        headers = {
            'user-agent': user_agent,
        }
        try:
            with session.get(url,
                             headers=headers,
                             timeout=3.5,
                             verify=False) as response:
                if(response.status_code == 200):
                    html_page = response.text
        except requests.exceptions.RequestException:
            pass
        finally:
            return html_page

    # Retrieve html responses from all sites

    def download_all_sites(self, sites):
        site_contents = []
        with requests.Session() as session:
            for url in sites:
                html_page = self.download_site(url, session)
                if html_page:
                    site_contents.append(html_page)
        return site_contents

    def filterTags(self, element, res):

        blacklist = ['style', 'label', '[document]', 'embed', 'img', 'object',
                     'noscript', 'header', 'iframe', 'audio', 'picture',
                     'meta', 'title', 'aside', 'footer', 'svg', 'base', 'figure',
                     'form', 'nav', 'head', 'link', 'button', 'source', 'canvas',
                     'br', 'input', 'script', 'wbr', 'video', 'param', 'hr', 'a', 'h1']
        # if the current tag is present
        # in blacklist
        if element.name in blacklist:
            return False
        # ignore the comments
        if isinstance(element, Comment):
            return False

        resText = element.find(text=True, recursive=False)
        if resText != None and resText.strip() not in ["", "\n", "\t", "!"]:
            res.append(resText)
        children = element.findChildren(recursive=False)
        if len(children) == 0:
            return False
        for child in children:
            self.filterTags(child, res)

    def text_from_html(self, htmlContent, res):
        import nltk
        from nltk.stem import PorterStemmer
        ps = PorterStemmer()

        soup = BeautifulSoup(htmlContent, 'html.parser')
        texts = soup.find()
        self.filterTags(texts, res)

        # getting only the relevant content
        # from urls based on query
        refined_content = []
        for sentence in res:
            for keyword in self.query_array:
                x = keyword.lower()
                y = keyword.upper()
                z = ps.stem(keyword)
                z1 = z.capitalize()
                z2 = z.upper()
                if ((x in sentence) or (y in sentence) or (z in sentence)
                        or (z1 in sentence) or (z2 in sentence)):
                    refined_content.append(sentence)
                    break
        return " ".join(t.strip() for t in refined_content)

    # Extract textual content from all pages

    def extract_text(self, extracted_site_contents):
        text_contents = []
        for html in extracted_site_contents:
            res = []
            page_text = self.text_from_html(html, res)
            if page_text is not None:
                text_contents.append(page_text)
        return text_contents

    # Get a list of relevant text documents for the input query

    def fetch_text_results(self, url):
        text_results = []
        links = []
        wiki_links, other_sites = [], []
        # URL list generation and bifurcation
        # Split the URLs into Wiki links and site links
        if "gstatic.com" not in url:  # Exclude static google content
            target = wiki_links if "en.wikipedia.org" in url else other_sites
            target.append(url)
            links.append(url)
            # Fetching Wiki pages
            wiki_pages = self.get_all_wikis(wiki_links)
            if wiki_pages:
                text_results += wiki_pages  # Merge wikis with text results
            # Fetching site HTMLs and extracting text
            site_pages = self.download_all_sites(
                other_sites)  # Get HTML from site URLs
            if site_pages:  # Emptiness check
                page_texts = self.extract_text(
                    site_pages)  # Extract texts from HTML
                if page_texts:  # Emptiness check
                    text_results += page_texts  # Merge site texts with text results
        return (text_results, links)

    # this functiom uses google search function
    # to get top urls and also encorporates
    # multiprocessing for scraping the urls
    def process(self, query):
        import multiprocessing
        # Set is used to keep only unique urls
        sites1 = set()
        # Search Google
        sites = self.google_search(
            query, num_results=3)  # Obtain the top 3 URLs
        # removing duplicate links
        # from list of urls
        for i in sites:
            found = -100
            found = i.find('?')
            if(found != -1):
                sites1.add(i[:found])
            else:
                sites1.add(i)

        results = []
        links = []
        # multiprocessing
        processPool = multiprocessing.Pool(3)
        for result, link in processPool.map(self.fetch_text_results, sites1):
            results += result
            links += link
        return results, links
