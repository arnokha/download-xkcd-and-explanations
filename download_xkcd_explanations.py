import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

# Create the output directory if it doesn't exist
output_dir = './outputs'
os.makedirs(output_dir, exist_ok=True)

# Define the CSV file path
csv_file = os.path.join(output_dir, 'xkcd_explanations.csv')

# Load existing data if the CSV file exists
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=['URL', 'Publish date', 'Explanation'])

index = 1  # Start from the first comic

while True:
    url = f'https://www.explainxkcd.com/wiki/index.php/{index}'
    print(f'Processing {url}')
    # Skip if the URL already exists in the DataFrame
    if url in df['URL'].values:
        print(f'URL {url} already exists, skipping.')
        index += 1
        continue
    
    try:
        response = requests.get(url)
        # Stop if the page does not exist
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



    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the Explanation section exists
    explanation_heading = soup.find('span', id='Explanation')
    index_exceptions = [819, 2408]
    if not explanation_heading:
        if index in index_exceptions:
            print("Non-standard format, skipping...")
            index += 1
            time.sleep(2)
            continue
        print(f'No Explanation section found at index {index}, stopping.')
        break

    # Extract Publish date
    publish_date = ''
    comic_content_table = soup.find('table', class_='comic-content')
    if comic_content_table:
        external_links = comic_content_table.find_all('a', class_='external text')
        for link in external_links:
            span = link.find('span')
            if span and 'Comic' in span.text:
                # Extract the date from the text
                text = span.text.strip()
                # The date is within parentheses
                if '(' in text and ')' in text:
                    date_part = text[text.find('(')+1:text.find(')')]
                    publish_date = date_part.replace('\xa0', ' ')
                    # Remove extra spaces
                    publish_date = re.sub(r'\s+', ' ', publish_date)
                break

    # Extract Explanation
    explanation = ''
    # Find the Explanation heading
    explanation_heading = soup.find('span', id='Explanation')
    # Get the parent h2 tag
    h2_tag = explanation_heading.find_parent('h2')
    # Get all siblings after the h2 tag
    sibling = h2_tag.find_next_sibling()
    explanation_paragraphs = []
    while sibling:
        if sibling.name == 'h2':
            break  # Stop if the next h2 tag is found
        if sibling.name == 'p':
            # Extract text with spaces between tags
            paragraph_text = sibling.get_text(separator=' ', strip=True)
            # Replace multiple spaces with a single space
            paragraph_text = re.sub(r'\s{2,}', ' ', paragraph_text)
            # Remove spaces before punctuation marks
            paragraph_text = re.sub(r'\s+([.,!?;:\'\"\)\]])', r'\1', paragraph_text)
            explanation_paragraphs.append(paragraph_text)
        sibling = sibling.find_next_sibling()
    # Combine paragraphs with delimiter
    explanation = '\n\n'.join(explanation_paragraphs)

    # Add the new data to the DataFrame
    new_row = {
        'URL': url,
        'Publish date': publish_date,
        'Explanation': explanation
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save the DataFrame to CSV
    df.to_csv(csv_file, index=False)
    print(f'Explanation for comic {index} added.')

    index += 1
    time.sleep(2)  # Sleep for 2 seconds between requests
