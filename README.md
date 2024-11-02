# XKCD Comics and Explanations Downloader

This repository contains two Python scripts that download XKCD comics and their corresponding explanations from [xkcd.com](https://xkcd.com) and [explainxkcd.com](https://www.explainxkcd.com), respectively.

## Scripts

1. **`download_xkcd_comic.py`**
   - **Description:** Downloads all XKCD comics, extracting the comic URL, image URL, title, and mouseover text.
   - **Output:** Saves the data to `./outputs/xkcd_comic.csv`.

2. **`download_xkcd_explanations.py`**
   - **Description:** Downloads explanations for all XKCD comics, including the publish date (if available) and the explanation text.
   - **Output:** Saves the data to `./outputs/xkcd_explanations.csv`.

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

   ```bash
   git clone https://github.com/yourusername/xkcd-downloader.git
   cd xkcd-downloader
   ```

2. **Run the Scripts**

   - **Download XKCD Comics:**

     ```bash
     python download_xkcd_comic.py
     ```

   - **Download XKCD Explanations:**

     ```bash
     python download_xkcd_explanations.py
     ```

   The scripts will create an `outputs` directory (if it doesn't exist) and save the CSV files there. They will resume from where they left off if run multiple times.

## Notes

- Each script pauses for 2 seconds between requests to respect server load.
- The scripts check for existing entries in the CSV files to avoid duplicates.
- Ensure you have a stable internet connection while running the scripts.

## License

This project is licensed under the MIT License.