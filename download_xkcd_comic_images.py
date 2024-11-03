import pandas as pd
import os
import time
import requests
from urllib.parse import urlparse
import mimetypes

# Load the CSV file
df = pd.read_csv('./outputs/xkcd_comic.csv')

# Ensure the output directory exists
output_dir = './outputs/xkcd_images'
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    image_url = row['Image URL']
    comic_url = row['URL']
    
    # Check if image_url is valid (comic #1037 has multiple images and i think it's the only nan)
    if pd.isna(image_url):
        print(f"Image URL is missing from CSV, skipping.")
        continue
    
    # Extract index from URL (e.g., https://xkcd.com/{index}/)
    comic_index = comic_url.strip('/').split('/')[-1]
    if not comic_index.isdigit():
        print(f"Skipping invalid URL: {comic_url}")
        continue  # Skip if the index is not a number

    # Parse the image extension
    parsed_url = urlparse(image_url)
    image_extension = os.path.splitext(parsed_url.path)[1]  # Includes the dot
    if not image_extension:
        # Attempt to get the extension from the Content-Type header
        response = requests.head(image_url)
        content_type = response.headers.get('Content-Type')
        image_extension = mimetypes.guess_extension(content_type) or '.jpg'  # Default to .jpg

    image_filename = f"{comic_index}{image_extension}"
    image_path = os.path.join(output_dir, image_filename)

    # Check if the image already exists
    if os.path.exists(image_path):
        print(f"Image {image_filename} already exists, skipping.")
        continue

    # Download the image
    try:
        print(f"Downloading {image_url} to {image_path}")
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors
        with open(image_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")

    # Sleep for 2 seconds before the next request
    time.sleep(2)

