# XKCD Comics and Explanations Downloader

This repository contains Python scripts that download XKCD comics and their corresponding explanations from [xkcd.com](https://xkcd.com) and [explainxkcd.com](https://www.explainxkcd.com).

## Scripts

1. **`download_xkcd_comic_info.py`**
   - **Description:** Downloads all XKCD comics, extracting the comic URL, image URL, title, and mouseover text.
   - **Output:** Saves the data to `./outputs/xkcd_comic.csv`.

2. **`download_xkcd_explanations.py`**
   - **Description:** Downloads explanations for all XKCD comics, including the publish date (if available) and the explanation text.
   - **Output:** Saves the data to `./outputs/xkcd_explanations.csv`.

3. **`download_xkcd_comic_images.py`**
   - **Description:** Downloads images for all XKCD comics, using the `Image URL` column of `./outputs/xkcd_comic.csv` (requires `download_xkcd_comic_info.py` run first)
   - **Output:** Saves the data to `./outputs/xkcd_images/{comic_number}.{file_extension}`.

## Requirements

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)

Install the required packages using:

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

1. **Clone the Repository**

2. **Run the Scripts**

   - **Download XKCD Comics:**

     ```bash
     python download_xkcd_comic_info.py
     ```

   - **Download XKCD Explanations:**

     ```bash
     python download_xkcd_explanations.py
     ```

    - **Download XKCD Explanations:** (requires `download_xkcd_comic_info.py` run first, to completion)

     ```bash
     python download_xkcd_comic_images.py
     ```

## Notes

- Each script pauses for 2 seconds between requests to respect server load.
- The scripts check for existing entries in the CSV files or existing images to avoid duplicates.
- Ensure you have a stable internet connection while running the scripts.

## License
This project is licensed under the MIT License.

## Other Licenses
xkcd is available under the [Creative Commons Attribution-NonCommercial 2.5 License](https://creativecommons.org/licenses/by-nc/2.5/).  
explainxkcd is available under the [Creative Commons Attribution-ShareAlike 3.0 license](https://creativecommons.org/licenses/by-nc/2.5/).