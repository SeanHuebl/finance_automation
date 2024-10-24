# Finance Automation

## Overview

The **Finance Automation** project is a Python-based tool designed to clean, categorize, and upload transaction data from multiple financial sources (such as Fidelity, Costco, and SoFi) to a Google Spreadsheet. The tool integrates with the Google Sheets API to automate data updates for financial tracking and reporting.

## Features

- **Data Wrangling**: Cleans and merges CSV files from multiple financial sources.
- **Categorization**: Automatically categorizes transactions into predefined categories (e.g., Food, Car, Housing, Medical).
- **Google Sheets Integration**: Securely uploads categorized data to a Google Spreadsheet using OAuth 2.0 authentication.
- **Automated Workflow**: Streamlines the entire process from data import to Google Sheets update.

## Learning Experience

This project was my first **non-guided** project. Through its development, I gained valuable insights into working with **pandas DataFrames** to manipulate data efficiently. I learned about using built in vectorization functions in order to perform looping actions quickly isntead of using native python loops. Additionally, this project introduced me to interacting with APIs, specifically working with **Google Cloud** and the **Google Sheets API** to automate data tasks. It was a rewarding challenge that significantly expanded my skill set in both data processing and cloud integration.

## Prerequisites

- **Python 3.8+** though I used 3.12
- **Google Cloud Project** with Google Sheets API enabled
- **Google OAuth 2.0 Client Credentials** (JSON file)
- **Google Spreadsheet** with corresponding tabs for each transaction category

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/finance_automation.git
    cd finance_automation
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Google OAuth 2.0 Credentials**:
    Here are the instructions to set up OAuth 2.0 credentials as a "Desktop" application and create the OAuth client secret in Google Cloud, formatted in Markdown for your README or documentation:

### Setting Up OAuth 2.0 Credentials

#### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. If you haven't already, sign in with your Google account.
3. Click on the **Select a Project** dropdown at the top of the page and click **New Project**.
4. Give your project a **Name** and click **Create**.
5. After creating the project, make sure it is selected.

#### Step 2: Enable the Google Sheets API

1. In the left-hand menu, go to **APIs & Services** > **Library**.
2. Search for **Google Sheets API** and click on it.
3. Click the **Enable** button.

#### Step 3: Set Up OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials** in the left-hand menu.
2. Click on the **+ CREATE CREDENTIALS** button and select **OAuth 2.0 Client ID**.
3. If prompted, configure your **OAuth consent screen**:
   - Select **External** and click **Create**.
   - Fill out the necessary information for the **OAuth consent screen** (e.g., App Name, User Support Email).
   - Click **Save and Continue** until you reach the summary page, then click **Back to Dashboard**.

#### Step 4: Create OAuth 2.0 Client ID

1. In the **Create OAuth client ID** form:
   - Choose **Application type** as **Desktop app**.
   - Provide a **Name** for your OAuth client (e.g., "Finance Automation Desktop Client").
2. Click **Create**.
3. A dialog will appear with your **Client ID** and **Client Secret**. Click **Download** to download the JSON file containing your OAuth 2.0 credentials. This file will be named something like `client_secret_<id>.json`.

#### Step 5: Save the OAuth Client Secret

1. Create a directory named `sensitive` within your project folder (if it doesn’t already exist).
2. Move the downloaded JSON file (`client_secret_<id>.json`) to the `sensitive` folder.
3. Rename the file to `client_secret_desktop.json` for consistency with the project code.

#### Step 6: Configure the Credentials in Your Code

Make sure your code references the JSON file in the correct location:

```python
flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
    './sensitive/client_secret_desktop.json', SCOPES
)
```
### Additional Links

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)


## Google Spreadsheet Setup

1. **Copy the Spreadsheet Template**:
   - Use the following link to open the [Google Spreadsheet Template](https://docs.google.com/spreadsheets/d/1T_-oDRsrrKe0pmfGlSkh59K80fc3AmMVJphW7OEh09A/edit?usp=sharing).
   - Click on `File > Make a copy` to create your own copy of the template.
   - Modify the spreadsheet as needed, ensuring that the tab names match the category names defined in the code.

2. **Update the Spreadsheet ID**:
   - Once you have created and modified your copy, update the `spreadsheet_id` variable in the code with your new Spreadsheet ID.
   - The spreadsheet id will be in the URL of the google doc. Example: https://docs.google.com/spreadsheets/d/**user_id**/edit?gid=595143441#gid=595143441

## Usage

### Using Sample CSV Files

This project includes three sample CSV files (`sample_fidelity.csv`, `sample_costco.csv`, `sample_sofi.csv`) located in the `csv` directory. You can modify the paths in the code to point to these CSV files to explore how the application works:

1. **Edit Paths in `wrangle_data.py`**:

    ```python
    df_fidelity: pd.DataFrame = clean_data_fidelity('./csv/sample_fidelity.csv')
    df_costco: pd.DataFrame = clean_data_costco('./csv/sample_costco.csv')
    df_sofi: pd.DataFrame = clean_data_sofi('./csv/sample_sofi.csv')
    ```

   These sample CSVs provide a basic understanding of how the application processes and categorizes data. For your own usage, you will need to modify the code based on the structure and content of your CSV files.

2. **Run the Application**:

    ```bash
    ./main.sh
    ```

3. **Authorize Access**:
   - When prompted, follow the URL provided in the console to authorize access via Google OAuth 2.0. This step is required to securely access the Google Sheets API.

4. **View Results**:
   - The processed transaction data will be uploaded to your specified Google Spreadsheet.

## Customizing for Your Own Use

To use this application with your own CSV files, you will need to:

- **Modify the CSV Paths**: Update the paths in the `_combine_data()` function to point to your own CSV files.
- **Adjust the `clean_data` Functions**: Depending on the structure of your own CSV files, you may need to modify or create new `clean_data` functions to handle specific formatting, columns, or naming conventions.

## Project Structure

```plaintext
finance_automation/
│
├── csv/                         # Folder for CSV files
│   ├── sample_fidelity.csv         # Sample CSV data for Fidelity
│   ├── sample_costco.csv           # Sample CSV data for Costco
│   └── sample_sofi.csv             # Sample CSV data for SoFi
│
├── sensitive/                   # Folder to store sensitive files (e.g., client secrets JSON)
│   └── client_secret_desktop.json  # Google OAuth 2.0 client credentials JSON
│
├── src/                         # Source code folder
│   ├── clean_data_fidelity.py       # Cleans and processes Fidelity CSV data
│   ├── clean_data_costco.py         # Cleans and processes Costco CSV data
│   ├── clean_data_sofi.py           # Cleans and processes SoFi CSV data
│   ├── categorize.py                # Categorizes transaction data into predefined categories
│   ├── google_cloud.py              # Handles Google Sheets API integration and data writing
│   ├── project_enums.py             # Defines Enums for transactions and categories
│   ├── wrangle_data.py              # Orchestrates data wrangling and merging of CSVs
│   └── main.py                      # Main script that executes the entire workflow
│
├── main.sh                     # Shell script to run the application
├── readme.md                   # Information on the program
└── requirements.txt            # Python dependencies