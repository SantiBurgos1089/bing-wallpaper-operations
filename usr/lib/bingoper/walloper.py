import requests
import json
from io import BytesIO
from PIL import Image

# The available markets that Bing actively serves localized wallpapers for.
# "en-ROW" stands for Rest of World.
BING_MARKET_CODES = [
    "en-US", "en-GB", "en-CA", 
    "en-AU", "en-NZ", "en-IN", 
    "en-ROW","zh-CN", "ja-JP", 
    "de-DE", "fr-FR", "fr-CA", 
    "it-IT", "es-ES", "pt-BR"
]

# The available resolutions. "UHD" will pull down the 4K version (3840x2160).
BING_RESOLUTIONS = [
    "UHD", "1920x1200", "1920x1080", 
    "1366x768", "1280x768", "1024x768", 
    "800x600", "800x480", "1080x1920", 
    "768x1280", "720x1280", "640x480", 
    "480x800", "400x240", "320x240", 
    "240x320"
]

class WallpaperProvider():
    pass

# ──────────────────────────────────────────────────────────────────────────────
# BingProvider: Provider to fetch wallpaper data from Microsoft Bing
# ──────────────────────────────────────────────────────────────────────────────
class BingProvider(WallpaperProvider):

    BING_BASE_URL = "https://www.bing.com"
    BING_API_URL = f"{BING_BASE_URL}/HPImageArchive.aspx"

    def get_wallpaper_data(self, region="Worldwide", img_resolution="1920x1080", days=0):
        # Prepare parameters for the JSON API endpoint
        url_params = {
            "format": "js",
            "idx": 0, # 0 = today, 1 = yesterday, etc.
            "n": 1 # Number of images to return
        }

        # Bing API only supports going back up to 7 days, higher values
        # will return the latest but we leave it as is for simplicity
        if days > 7:
            raise ValueError("Bing API only supports going back up to 7 days (idx=7).")

        # Apply the region if it's explicitly set and valid, otherwise
        # leave the region "Worldwide" as default
        if region != "Worldwide" and region in BING_MARKET_CODES:
            url_params["mkt"] = region

        # Ensure the resolution is valid, otherwise download and show a FullHD
        # resolution (1920x1080), even if the screen resolution might not be that
        if img_resolution not in BING_RESOLUTIONS:
            img_resolution = "1920x1080"

        try:
            # Make the initial request to the Bing Archive API
            bing_response = requests.get(self.BING_API_URL, params=url_params, timeout=15)
            bing_response.raise_for_status()
            bing_data = bing_response.json()

            if not bing_data.get("images"):
                raise ValueError("Bing API returned no images.")

            bing_image_info = bing_data["images"][0]

            # Construct the exact URL to download the unwatermarked picture
            bing_urlbase = bing_image_info.get("urlbase")
            exact_image_url = f"{self.BING_BASE_URL}{bing_urlbase}_{img_resolution}.jpg"

            # Download the actual image bytes into memory
            img_response = requests.get(exact_image_url, timeout=15)
            img_response.raise_for_status()
            image_bytes = img_response.content

            # Extract useful metadata to pass along to the UI or Database
            bing_metadata = {
                "title": bing_image_info.get("title", ""),
                "copyright": bing_image_info.get("copyright", ""),
                "exact_url": exact_image_url,
                "startdate": bing_image_info.get("startdate", "")
            }

            return image_bytes, bing_metadata

        except requests.exceptions.RequestException as e:
            print(f"Network error while fetching Bing wallpaper: {e}")
            return None, {}



class SpotlightProvider(WallpaperProvider):
    pass
