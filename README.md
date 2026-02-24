# Hashtag Video Scraper 📊
This program scrapes Tiktok video results from a given hashtag keyword using Playwright and outputs structured data for analysis.

## Project Structure 📁
.\
├── main.py                  # Handles user input and runs the scraper\
├── scrapper.py              # Core scraping logic\
├── requirements.txt         # Project dependencies\
├── .gitignore               # Excludes venv and unnecessary files\
└── README.md                # This file

## Prerequisites ✅ 
* Python 3.9 or higher
* pip (comes with Python)

To check your version, run the following on your local terminal: 
*python3 --version*


## Setup Instructions ⚙️
The following commands should be run in order on your local terminal:

### Clone the repository 1️⃣
*git clone https://github.com/abrodriguezalman/nuvora-tktk-scrapper.git* \
*cd nuvora-tktk-scrapper*

### Create a virtual environment (recommended) 2️⃣
Mac/Linux:\
*python3 -m venv venv*
*source venv/bin/activate*

Windows:\
*python -m venv venv*
*venv/Scripts/activate*


### Install dependencies 3️⃣
*pip install -r requirements.txt*

### Install Playwright browser binaries 4️⃣
This step is required for the scraper to launch Chromium.\
*playwright install chromium*

## Running the Program 🚀
After setup, run the following line:
*python main.py*

You will be prompted to enter a hashtag keyword.

The program will:
* Launch Chromium
* Scrape available video results
* Return structured data
* Exit cleanly (including if no results are found)

## Error Handling 🛑
If a hashtag yields no results:
* The program exits gracefully
* A helpful message is displayed
* The browser closes cleanly

If you encounter browser timeout errors:
* Ensure you ran playwright install chromium
* Make sure no zombie Chromium processes are running
* Restart your terminal and try again

## Notes for Leadership 🧠
* This program uses automated browser control (Playwright).
* First run may take slightly longer due to browser initialization.
* Do not delete the venv folder while using the program.
* If setup issues occur, deleting the venv folder and re-running setup usually resolves them.

## Dependencies 🧩
See requirements.txt for exact versions.
