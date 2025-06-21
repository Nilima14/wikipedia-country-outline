from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Name of the country")):
    """
    Fetch Wikipedia page and return Markdown outline of headings.
    """
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Wikipedia page for '{country}' not found."}

    soup = BeautifulSoup(response.text, "html.parser")

    markdown = f"## Contents\n\n# {country}\n"

    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(header.name[1])
        text = header.get_text(strip=True)
        if text.lower() not in ["contents", "navigation menu"]:
            markdown += f"{'#' * level} {text}\n\n"

    return {"outline": markdown.strip()}
