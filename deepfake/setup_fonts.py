"""
Script to download and set up required fonts
"""

import os
import requests
from pathlib import Path
import shutil

FONTS_DIR = Path("web_app/static/fonts")
FONTS_DIR.mkdir(exist_ok=True)

# Font URLs
FONT_URLS = {
    "DejaVuSansCondensed.ttf": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSansCondensed.ttf",
    "DejaVuSansCondensed-Bold.ttf": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSansCondensed-Bold.ttf"
}

def download_font(url: str, filename: str):
    """Download font file"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(FONTS_DIR / filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

def main():
    """Download all required fonts"""
    print("Downloading required fonts...")
    for filename, url in FONT_URLS.items():
        if not (FONTS_DIR / filename).exists():
            download_font(url, filename)
        else:
            print(f"{filename} already exists")
    print("Font setup complete!")

if __name__ == "__main__":
    main()
