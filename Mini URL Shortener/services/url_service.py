from sqlalchemy.orm import Session
from models.url import URLMapping
from utils.encoder import Base62Encoder
from urllib.parse import urlparse
import time

class URLService:
    """Business logic for URL shortening"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate if string is a valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def get_or_create_short_url(original_url: str, db: Session) -> str:
        """Get existing short code or create new one using hash"""
        
        # Check if URL already exists
        existing = db.query(URLMapping).filter(
            URLMapping.original_url == original_url
        ).first()
        
        if existing:
            return existing.short_code
        
        # Generate hash-based short code
        short_code = Base62Encoder.generate_hash_code(original_url, length=6)
        
        # Handle collision: if short_code already exists, add timestamp
        max_attempts = 10
        attempt = 0
        original_short_code = short_code
        
        while attempt < max_attempts:
            existing_code = db.query(URLMapping).filter(
                URLMapping.short_code == short_code
            ).first()
            
            if not existing_code:
                # Short code is unique, we can use it
                break
            
            # Collision detected! Generate new code by adding timestamp
            collision_string = original_url + str(time.time()) + str(attempt)
            short_code = Base62Encoder.generate_hash_code(collision_string, length=6)
            attempt += 1
        
        # If still collision after max attempts (very unlikely), add random suffix
        if attempt >= max_attempts:
            short_code = original_short_code + str(attempt)
        
        # Store in database
        url_mapping = URLMapping(
            original_url=original_url,
            short_code=short_code
        )
        db.add(url_mapping)
        db.commit()
        db.refresh(url_mapping)
        
        return short_code
    
    @staticmethod
    def get_original_url(short_code: str, db: Session):
        """Get original URL by short code and increment click count"""
        url_mapping = db.query(URLMapping).filter(
            URLMapping.short_code == short_code
        ).first()
        
        if url_mapping:
            url_mapping.click_count += 1
            db.commit()
        
        return url_mapping