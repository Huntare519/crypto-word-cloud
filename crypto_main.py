# cmd-shift-p to reload vscode window
import yaml
import os
import re
from dotenv import load_dotenv
#import pandas as pd
from crypto_driver import Driver

# import yaml file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# loading .env file
load_dotenv()


def write_to_file(data):
    cwd = os.getcwd() + ("/all_jobs.csv")
    file = open('all_jobs.csv', 'w')
    for items in data:
        # creating a csv
        file.write(items[0].replace(", ", "-") + ",")
        file.write('\n')
    file.close()


def create_best_file(data):
    banned_words = ['your', 'role', 'not', 'listed',
                    'apply', 'here', 'general', 'application']
    pattern = '^[A-Za-z0-9]*$'  # filter out special characters
    file = open('lineByline.csv', 'w')
    for items in data:
        # creating a csv
        words = items[0].split(" ")
        for word in words:
            if word.lower() not in banned_words and re.match(pattern, word):
                file.write(word + ",")
                file.write('\n')
    file.close()


def clean_file():
    pass


def count_num_companies():
    count = 0
    for k, v in config.items():
        for companies in v:
            count += 1
    return count


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
    #data = format_data(matching_jobs)
    write_to_file(matching_jobs)
    create_best_file(matching_jobs)
    driver.quit()
