# Application settings (like application.properties in Spring Boot)

APP_TITLE = "InfoLens AI Service"
APP_DESCRIPTION = "AI microservice for Indian news intelligence"
APP_VERSION = "0.1.0"

# Frontend URL for CORS
FRONTEND_URL = "http://localhost:4200"

# News sources — NOT hardcoded with bias labels
# Bias will be estimated dynamically by AI
NEWS_SOURCES = [
    {"name": "The Hindu", "category": "Mainstream", "rss_url": "https://www.thehindu.com/feeder/default.rss"},
    {"name": "Indian Express", "category": "Mainstream", "rss_url": "https://indianexpress.com/feed/"},
    {"name": "NDTV", "category": "Mainstream", "rss_url": "https://feeds.feedburner.com/ndtvnews-top-stories"},
    {"name": "Times of India", "category": "Mainstream", "rss_url": ""},
    {"name": "Republic TV", "category": "English", "rss_url": ""},
    {"name": "Zee News", "category": "English", "rss_url": ""},
    {"name": "India TV", "category": "English", "rss_url": ""},
    {"name": "OpIndia", "category": "Digital", "rss_url": "https://www.opindia.com/feed/"},
    {"name": "Swarajya", "category": "Digital", "rss_url": "https://swarajyamag.com/feed"},
    {"name": "The Wire", "category": "Digital", "rss_url": "https://thewire.in/feed"},
    {"name": "Scroll", "category": "Digital", "rss_url": "https://scroll.in/feed"},
    {"name": "Newslaundry", "category": "Digital", "rss_url": ""},
    {"name": "The News Minute", "category": "Digital", "rss_url": "https://www.thenewsminute.com/feed"},
    {"name": "Alt News", "category": "Fact-check", "rss_url": ""},
]

# Ollama local LLM
OLLAMA_BASE_URL = "http://localhost:11434"
