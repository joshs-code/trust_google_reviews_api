from fastapi import FastAPI
from google_scraper import GoogleScraper
import uvicorn

app = FastAPI()

@app.get("/all/{urlpath:path}")
async def all_reviews(urlpath: str):
    data = GoogleScraper().get_all(urlpath)
    return data

@app.get("/reviews/8/{urlpath:path}")
async def ten_reviews(urlpath: str):
    data = GoogleScraper().get_eight_reviews(urlpath)
    return data


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)