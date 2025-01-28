import requests
from bs4 import BeautifulSoup
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentScraper:
    def __init__(self):
        self.session = requests.Session()
        
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
        except Exception as e:
            logger.error(f"Error searching documentation: {str(e)}")
            return []

    def _parse_search_results(self, soup):
        results = []
        for result in soup.find_all('div', class_='search-result'):
            results.append({
                'title': result.find('h3').text.strip(),
                'url': result.find('a')['href'],
                'snippet': result.find('p').text.strip()
            })
        return results
