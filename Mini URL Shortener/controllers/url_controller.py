from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from config.settings import SessionLocal
from services.url_service import URLService

class URLController:
    """Handle URL shortening requests"""
    
    @staticmethod
    def shorten_url(url: str):
        """Create a short URL"""
        db = SessionLocal()
        try:
            # Validate URL
            if not URLService.is_valid_url(url):
                raise HTTPException(status_code=400, detail="Invalid URL format")
            
            # Get or create short code
            short_code = URLService.get_or_create_short_url(url, db)
            
            return {
                "original_url": url,
                "short_code": short_code,
                "short_url": f"http://localhost:8000/{short_code}"
            }
        finally:
            db.close()
    
    @staticmethod
    def redirect_to_original(short_code: str):
        """Redirect to original URL"""
        db = SessionLocal()
        try:
            url_mapping = URLService.get_original_url(short_code, db)
            
            if not url_mapping:
                raise HTTPException(status_code=404, detail="Short code not found")
            
            return RedirectResponse(url=url_mapping.original_url, status_code=302)
        finally:
            db.close()