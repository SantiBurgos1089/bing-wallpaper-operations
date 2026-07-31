import requests
import json
from io import BytesIO
from PIL import Image

# The available markets that Bing actively serves localized wallpapers for.
# "en-ROW" stands for Rest of World.
BING_MARKET_CODES = [
    "en-US", "en-GB", "en-CA", "en-AU", "en-NZ", "en-IN", "en-ROW",
    "zh-CN", "ja-JP", "de-DE", "fr-FR", "fr-CA", "it-IT", "es-ES", "pt-BR"
]

# The available resolutions. "UHD" will pull down the 4K version (3840x2160).
BING_RESOLUTIONS = [
    "UHD", "1920x1200", "1920x1080", "1366x768", "1280x768",
    "1024x768", "800x600", "800x480", "1080x1920", "768x1280", 
    "720x1280", "640x480", "480x800", "400x240", "320x240", "240x320"
]

class WallpaperProvider:
    pass

class BingProvider(WallpaperProvider):
    pass

class SpotlightProvider(WallpaperProvider):
    pass
