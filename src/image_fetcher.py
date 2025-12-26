# src/image_fetcher.py
import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class ImageFetcher:
    def __init__(self):
        self.access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        self.fallback_images = {
            "title": "assets/default_images/title_bg.jpg",
            "section": "assets/default_images/section_bg.jpg",
            "content": "assets/default_images/content_bg.jpg"
        }

    def fetch_image(self, query: str, save_path: str) -> str:
        """
        Fetch an image from Unsplash based on the query and save locally.
        Returns the path to the saved image.
        """
        if not self.access_key:
            logger.warning("UNSPLASH_ACCESS_KEY not found, using fallback")
            return self._create_fallback_image(query, save_path)

        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": query,
            "client_id": self.access_key,
            "orientation": "landscape"
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            image_url = data['urls']['regular']

            # Download the image
            img_response = requests.get(image_url, timeout=10)
            img_response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(img_response.content)
            
            logger.info(f"Image saved to {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching image for '{query}': {e}")
            return self._create_fallback_image(query, save_path)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return self._create_fallback_image(query, save_path)

    def _create_fallback_image(self, query: str, save_path: str) -> str:
        """Create a simple fallback image with text"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        img = Image.new('RGB', (800, 600), color=(74, 144, 226))
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("assets/fonts/arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Draw the query text
        text = query[:30] + "..." if len(query) > 30 else query
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (800 - text_width) / 2
        y = (600 - text_height) / 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        img.save(save_path)
        
        return save_path