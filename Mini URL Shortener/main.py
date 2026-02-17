from fastapi import FastAPI, Request, Form
from config.settings import engine, Settings
from models.url import Base
from routes.url_routes import router
from fastapi.middleware.cors import CORSMiddleware
# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title=Settings.APP_NAME,
    version=Settings.APP_VERSION,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    """Health check"""
    return {"message": "URL Shortener API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

app= FastAPI()
