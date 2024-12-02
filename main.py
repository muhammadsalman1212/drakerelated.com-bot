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
# pip install playwright
# playwright install
# pip install pandas, requests
import time
from datetime import datetime

df = pd.read_csv("emails.csv")
email_list = df['Emails'].tolist()
print(email_list)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for all_emails in email_list:
        page.goto("https://drakerelated.com/pages/tour", timeout=0)

        # i want to fill the input with email

        #email
        page.fill('input[name="email"]', all_emails, timeout=0)

        submit = page.click("//button[text()='Submit']", timeout=0)

        time.sleep(6)

    page.close()
