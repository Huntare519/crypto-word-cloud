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


def count_num_companies():
    count = 0
    for items in config:
        for company in items:
            print(item)
            count += 1
    return count


# this link: https://monkeylearn.com/word-cloud/
# takes a comma seperated list and returns the word cloud
if __name__ == "__main__":
    matching_jobs = list()
    for company in config['companies']:
        driver = Driver(company['keywords'], company['name'],
                        company['url'], company['job-posting-tag'], company['job-board-type'])
        driver.open_chrome()
        driver.load_page()

        if company['job-board-type'] == 'lever':
            matching_jobs.extend(driver.handle_lever())
        elif company['job-board-type'] == 'greenhouse' or company['job-board-type'] == 'greenhouse-type':
            matching_jobs.extend(driver.handle_greenhouse())
        elif company['job-board-type'] == 'custom':
            matching_jobs.extend(driver.handle_url_mutation())

    print("length of list:", len(matching_jobs))
    print("number of companies scraped:", count_num_companies())
    data = format_data(matching_jobs)
    driver.quit()
