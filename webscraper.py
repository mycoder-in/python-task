import requests
from bs4 import BeautifulSoup

# URL of a sample news website (you can replace this with any news site)
URL = "https://www.bbc.com/news"

# Step 1: Fetch the HTML
response = requests.get(URL)
if response.status_code != 200:
    print("Failed to fetch webpage")
    exit()

# Step 2: Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Example: Headlines are usually inside <h2> tags
headlines = soup.find_all("h2")

# Step 3: Extract text and save to a file
with open("headlines.txt", "w", encoding="utf-8") as f:
    for i, h in enumerate(headlines, 1):
        headline_text = h.get_text(strip=True)
        if headline_text:  # avoid empty lines
            f.write(f"{i}. {headline_text}\n")

print("✅ Headlines scraped and saved to headlines.txt")
