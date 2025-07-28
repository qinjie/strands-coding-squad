from datetime import datetime

class Article:
    """
    Model class for news articles
    """
    def __init__(self, article_data):
        self.source_id = article_data.get('source', {}).get('id')
        self.source_name = article_data.get('source', {}).get('name')
        self.author = article_data.get('author')
        self.title = article_data.get('title')
        self.description = article_data.get('description')
        self.url = article_data.get('url')
        self.url_to_image = article_data.get('urlToImage')
        self.published_at = article_data.get('publishedAt')
        self.content = article_data.get('content')
        
    @property
    def formatted_date(self):
        """
        Format the published date in a human-readable format
        """
        if not self.published_at:
            return "Unknown date"
        
        try:
            date_obj = datetime.strptime(self.published_at, "%Y-%m-%dT%H:%M:%SZ")
            return date_obj.strftime("%B %d, %Y at %H:%M")
        except ValueError:
            return self.published_at
            
    @property
    def short_description(self):
        """
        Return a shortened version of the description for card display
        """
        if not self.description:
            return "No description available"
        
        if len(self.description) > 150:
            return self.description[:150] + "..."
        return self.description
        
    @property
    def default_image(self):
        """
        Return a default image URL if no image is available
        """
        if self.url_to_image:
            return self.url_to_image
        return "/static/img/default-news.jpg"