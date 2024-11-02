import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Create the output directory if it doesn't exist
output_dir = './outputs'
os.makedirs(output_dir, exist_ok=True)

# Define the CSV file path
csv_file = os.path.join(output_dir, 'xkcd_comic.csv')

# Load existing data if the CSV file exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=['URL', 'Image URL', 'Title', 'Mouseover text'])

index = 1  # Start from the first comic

while True:
    url = f'https://xkcd.com/{index}/'
    print(f'Processing {url}')
    try:
        response = requests.get(url)
        # Stop if a 404 error is encountered
        if response.status_code == 404:
            print(f'404 error at index {index}, stopping.')
            break
        elif response.status_code != 200:
            print(f'Error {response.status_code} at index {index}, skipping.')
            index += 1
            time.sleep(2)
            continue
    except requests.exceptions.RequestException as e:
        print(f'Request failed at index {index}: {e}')
        index += 1
        time.sleep(2)
        continue

    # Skip if the URL already exists in the DataFrame
    if url in df['URL'].values:
        print(f'URL {url} already exists, skipping.')
        index += 1
        time.sleep(2)
        continue

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract Title
    title_div = soup.find('div', id='ctitle')
    title = title_div.text.strip() if title_div else ''

    # Extract Image URL
    image_url = ''
    middle_container = soup.find('div', id='middleContainer')
    if middle_container:
        anchors = middle_container.find_all('a', href=True)
        for a in anchors:
            href = a['href']
            if href.startswith('https://imgs.xkcd.com/'):
                image_url = href
                break

    # Extract Mouseover text
    mouseover_text = ''
    comic_div = soup.find('div', id='comic')
    if comic_div:
        img = comic_div.find('img')
        if img and img.has_attr('title'):
            mouseover_text = img['title']

    # Add the new data to the DataFrame
    new_row = {
        'URL': url,
        'Image URL': image_url,
        'Title': title,
        'Mouseover text': mouseover_text
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save the DataFrame to CSV
    df.to_csv(csv_file, index=False)
    print(f'Comic {index} added.')

    index += 1
    time.sleep(2)  # Sleep for 2 seconds between requests
