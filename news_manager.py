import json

class NewsArticle:
    """Respresents a single news article"""

    def __init__(self,title,source,content,category):
        self.title = title
        self.source = source
        self.content = content
        self.category = category

    def to_dict(self):
        """Convert object to dictionary (useful for JSON)."""
        return {
            "title": self.title,
            "source": self.source,
            "content": self.content,
            "category": self.category
        }
    
    def __str__(self):
        return f"[{self.source}] {self.title}"
    
class NewsManager:
    """Manages multiple news articles."""

    def __init__(self):
        self.articles = [] # list to store articles

    def add_article(self,article):
        """Add a NewsArticle to the list."""
        if isinstance(article,NewsArticle):
            self.articles.append(article)
        else:
            raise TypeError("Only NewsArticle objects allowed")
        
    def get_by_source(self,source_name):
        """Return all articles from a specific source."""
        return [a for a in self.articles if a.source == source_name]
    
    def to_json(self):
        """Convert all artciles to JSON string."""
        return json.dumps([a.to_dict() for a in self.articles], indent=2)
    
# ------------------ TESTING ------------------

if __name__ == "__main__":
    manager = NewsManager()

    # Create 5 sample Indian news articles
    a1 = NewsArticle(
        "Budget 2025 Highlights",
        "The Hindu",
        "Finance Minister announces major tax reforms.",
        "Finance"
    )

    a2 = NewsArticle(
        "India Wins Cricket Series",
        "ESPN Cricinfo",
        "India defeats Australia 3-1 in the series.",
        "Sports"
    )

    a3 = NewsArticle(
        "Heavy Rain in Delhi",
        "NDTV",
        "Waterlogging reported in several areas.",
        "Weather"
    )

    a4 = NewsArticle(
        "New Education Policy Update",
        "Indian Express",
        "Government introduces new digital learning initiatives.",
        "Education"
    )

    a5 = NewsArticle(
        "Startup Boom in Bengaluru",
        "Economic Times",
        "Tech startups see record funding this quarter.",
        "Business"
    )

    # Add articles
    manager.add_article(a1)
    manager.add_article(a2)
    manager.add_article(a3)
    manager.add_article(a4)
    manager.add_article(a5)

    # Test get_by_source
    print("Articles from NDTV:")
    ndtv_articles = manager.get_by_source("NDTV")
    for art in ndtv_articles:
        print(art)

    # Test JSON output
    print("\nAll Articles in JSON:")
    print(manager.to_json())