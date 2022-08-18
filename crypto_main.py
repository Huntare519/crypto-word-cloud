from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# cmd-shift-p to reload vscode window
from pretty_html_table import build_table
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import yaml
import os
from dotenv import load_dotenv
import pandas as pd
from crypto_driver import Driver

# import yaml file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# loading .env file
load_dotenv()


def format_data(matching_jobs: list):
    data = pd.DataFrame(matching_jobs, columns=[
                        "Job Title", 'Company Name', 'Link'])
    return data


if __name__ == "__main__":
    matching_jobs = list()
    for company in config['companies']:
        driver = Driver(company['keywords'], company['name'],
                        company['url'], company['job-posting-tag'], company['job-board-type'])
        driver.open_chrome()
        driver.load_page()

        if company['job-board-type'] == 'lever':
            matching_jobs.extend(driver.handle_lever())
        elif company['job-board-type'] == 'greenhouse':
            matching_jobs.extend(driver.handle_greenhouse())
        elif company['job-board-type'] == 'custom':
            matching_jobs.extend(driver.handle_url_mutation())

    print("lenght of list:", len(matching_jobs))
    data = format_data(matching_jobs)
    driver.quit()
