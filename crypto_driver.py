from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class Driver:
    def __init__(self, keywords, company, url, tag_name, job_board_type, *args, **kwargs):
        self.driver = None
        self.keywords = keywords
        self.company = company
        self.tag_name = tag_name
        self.url = url
        self.pagination = True
        self.job_board_type = job_board_type

    def open_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def load_page(self):
        self.driver.get(self.url)
        time.sleep(5)

    def quit(self):
        self.driver.quit()

    def handle_lever(self):
        self.driver.maximize_window()
        time.sleep(5)
        titles = self.driver.find_elements(
            By.CLASS_NAME, "posting-title")

        matching_results = list()

        for title in titles:
            job = title.find_element(By.TAG_NAME, "h5")
            link = title.get_attribute("href")
            for keyword in self.keywords:
                if keyword in job.text:
                    matching_results.append([job.text, self.company, link])
        return matching_results

    def handle_greenhouse(self):
        self.driver.maximize_window()
        time.sleep(5)
        jobs = self.driver.find_elements(By.CLASS_NAME, "opening")

        matching_results = list()

        for job in jobs:
            link = job.find_element(By.TAG_NAME, "a")
            for keyword in self.keywords:
                if keyword in job.text:
                    job_title = job.text.split("\n")
                    matching_results.append(
                        [job_title[0], self.company, link.get_attribute('href')])
        return matching_results

    def handle_url_mutation(self):
        matches = list()
        for key in self.keywords:
            self.driver.get(f"{self.url}?search={key}")
            WebDriverWait(self.driver, timeout=10).until(
                lambda d: d.find_elements(By.TAG_NAME, self.tag_name))
            time.sleep(5)
            found_jobs = self.driver.find_elements(
                By.TAG_NAME, self.tag_name)
            for job in found_jobs:
                matches.append(job.text)

        matching_results = list()
        for job in matches:
            for keyword in self.keywords:
                if keyword in job:
                    matching_results.append(
                        [job, self.company, self.url])
        return matching_results
