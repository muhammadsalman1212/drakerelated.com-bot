import glob
import json
import os
import random
import time
import shutil
from pathlib import Path
import csv
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime

# Function to read CSV and extract emails
def extract_emails_from_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist!")
    try:
        df = pd.read_csv(file_path)
        if 'Emails' not in df.columns:
            raise ValueError("CSV file does not contain 'Emails' column!")
        return df['Emails'].tolist()
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the CSV: {e}")

# Function to perform email submission on the webpage
def submit_email(page, email):
    try:
        page.goto("https://drakerelated.com/pages/tour", timeout=0)
        page.fill('input[name="email"]', email, timeout=0)
        # Click submit button
        page.click("//button[text()='Submit']", timeout=0)
        print(f"Email {email} submitted successfully.")
        time.sleep(6)
    except Exception as e:
        print(f"Failed to submit email {email}: {e}")

# Main automation logic
def main():
    csv_path = "emails.csv"
    try:
        email_list = extract_emails_from_csv(csv_path)
        print(f"Extracted {len(email_list)} emails.")
    except Exception as e:
        print(f"Error during email extraction: {e}")
        return

    with sync_playwright() as playwright_instance:
        try:
            browser = playwright_instance.chromium.launch(headless=False)
            page = browser.new_page()

            for email in email_list:
                submit_email(page, email)

            page.close()
            browser.close()
        except Exception as e:
            print(f"An error occurred during browser operation: {e}")

if __name__ == "__main__":
    print(f"Script started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(random.randint(1, 3))
    main()
    print(f"Script ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
