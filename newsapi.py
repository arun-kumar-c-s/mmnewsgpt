import requests

class NewsAPI:

    def __init__(self, api_key):
        """
        Initialize the NewsAPI client with the provided API key.
        
        :param api_key: Your NewsAPI.org API key
        """
        self.base_url = "https://newsapi.org/v2"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        self.CATEGORIES = [
        'business', 'entertainment', 'general', 
        'health', 'science', 'sports', 'technology']

        self.LANGUAGES = [
            'ar', 'de', 'en', 'es', 'fr', 'he', 
            'it', 'nl', 'no', 'pt', 'ru', 'sv', 
            'ud', 'zh']

        self.COUNTRIES = [
            'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 
            'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 
            'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 
            'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 
            'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 
            'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 
            'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 
            'tw', 'ua', 'us', 've', 'za']


    def get_everything(self, query, **kwargs):
        """
        Search through millions of articles from various sources.
        
        :param query: Keywords or phrases to search for
        :param kwargs: Optional additional parameters like:
            - sources: A comma-separated string of source ids
            - from_date: Articles from this date (YYYY-MM-DD)
            - to_date: Articles to this date (YYYY-MM-DD)
            - language: The 2-letter ISO-639-1 code of the language
            - sort_by: relevancy, popularity, publishedAt
            - page_size: Number of results to return per page
            - page: Page number of results
        :return: JSON response from NewsAPI
        """
        endpoint = f"{self.base_url}/everything"
        params = {"q": query, **kwargs}
        
        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

    def get_top_headlines(self, country=None, category=None, sources=None, **kwargs):
        """
        Get top headlines from news sources and blogs.
        
        :param country: The 2-letter ISO 3166-1 code of the country
        :param category: Business, entertainment, general, health, science, sports, technology
        :param sources: A comma-separated string of source ids
        :param kwargs: Additional optional parameters like page_size, page
        :return: JSON response from NewsAPI
        """
        endpoint = f"{self.base_url}/top-headlines"
        
        # Prepare parameters, only include non-None values
        params = {k: v for k, v in {
            "country": country, 
            "category": category, 
            "sources": sources, 
            **kwargs
        }.items() if v is not None}
        
        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching top headlines: {e}")
            return None

    def get_sources(self, category=None, language=None, country=None):
        """
        Retrieve news sources available on NewsAPI.
        
        :param category: Business, entertainment, general, health, science, sports, technology
        :param language: The 2-letter ISO-639-1 code of the language
        :param country: The 2-letter ISO 3166-1 code of the country
        :return: JSON response from NewsAPI
        """
        endpoint = f"{self.base_url}/sources"
        
        # Prepare parameters, only include non-None values
        params = {k: v for k, v in {
            "category": category, 
            "language": language, 
            "country": country
        }.items() if v is not None}
        
        try:
            response = requests.get(endpoint, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news sources: {e}")
            return None

