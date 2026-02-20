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
$\color{blue}{python3 --version}$

## Setup Instructions ⚙️
The following commands should be run in order on your local terminal:

### Clone the repository 1️⃣
$\color{blue}{git \space clone \space<your-repo-url>}$\
$\color{blue}{cd \space<repo-name>}$

### Create a virtual environment (recommended) 2️⃣
Mac/Linux:\
$\color{blue}{python3 \space -m \space venv \space venv}$\
$\color{blue}{source \space venv/bin/activate}$

Windows:\
$\color{blue}{python \space -m \space venv \space venv}$\
$\color{blue}{venv\Scripts\activate}$

### Install dependencies 3️⃣
$\color{blue}{pip \space install \space -r \space requirements.txt}$

### Install Playwright browser binaries 4️⃣
This step is required for the scraper to launch Chromium.\
$\color{blue}{playwright \space install \space chromium}$

## Running the Program 🚀
After setup, run the following line:
$\color{blue}{python \space main.py}$

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
