from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MarketData(BaseModel):
    """
    Pydantic model for validating incoming market data.
    """
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, GOOGL)")
    timestamp: datetime = Field(..., description="Timestamp of the market data")
    price: float = Field(..., gt=0, description="Price of the stock at the given timestamp")
    volume: int = Field(..., gt=0, description="Trading volume at the given timestamp")
    source: str = Field(..., description="Source of the market data (e.g., Bloomberg, Reuters)")
    
    optional_field: Optional[str] = Field(None, description="Optional field for additional information")

class NewsArticle(BaseModel):
    """
    Pydantic model for validating news article data.
    """
    title: str = Field(..., description="Title of the news article")
    url: str = Field(..., description="URL of the news article")
    publication_date: datetime = Field(..., description="Date when the article was published")
    content_summary: str = Field(..., description="Brief summary of the article content")
    source: str = Field(..., description="Source of the news article (e.g., Reuters, WSJ)")
