import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentScraper:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
    def search_documentation(self, query, base_url):
        """
        Search documentation for relevant information.
        """
        try:
            response = self.session.get(f"{base_url}/search", params={"q": query})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = self._parse_search_results(soup)
            
            return results
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error searching documentation: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return []

    def _parse_search_results(self, soup):
        results = []
        for result in soup.find_all('div', class_='search-result'):
            title = result.find('h3')
            link = result.find('a')
            snippet = result.find('p')
            if title and link and snippet:
                results.append({
                    'title': title.text.strip(),
                    'url': link.get('href'),
                    'snippet': snippet.text.strip()
                })
        return results
