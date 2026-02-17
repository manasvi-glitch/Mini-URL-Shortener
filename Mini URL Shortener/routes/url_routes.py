from fastapi import APIRouter, Query
from controllers.url_controller import URLController

router = APIRouter()

@router.post("/shorten")
async def shorten_url(url: str = Query(..., description="Long URL to shorten")):
    """Create a short URL"""
    return URLController.shorten_url(url)

@router.get("/{short_code}")
async def redirect_url(short_code: str):
    """Redirect to original URL"""
    return URLController.redirect_to_original(short_code)