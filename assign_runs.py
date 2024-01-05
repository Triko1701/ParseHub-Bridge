# import os
# import sys
# current_dir = os.path.dirname(__file__)
# base_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
# models_dir = os.path.join(base_dir, r'slave\app\models')
# sys.path.append(models_dir)
# import Run

# print(Run)

import re
import time
import math

import pandas as pd
import requests
from bs4 import BeautifulSoup

from . import app
from .app.extensions import db
from .app.models.Run import Run
from .utils.vm_metadata_extraction import get_vm_meta_field
from .utils.time import get_current_time

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url


def get_total_jobs_count(job_search_url):
  time.sleep(0.5)
  response = requests.get(job_search_url)
  
  if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the span element with data-automation="totalJobsCount"
    total_jobs_element = soup.find("span", {"data-automation": "totalJobsCount"})
    
    if total_jobs_element:
      # Extract the job count text
      total_jobs_count = total_jobs_element.get_text()
      return int(total_jobs_count)
    print("Could not parse total jobs count")
  
  else:
    print("Failed to fetch the web page.")
    
  return 0


def get_urls(base_urls):
  # Salary ranges
  salary_limits = ["30", "40", "50", "60", "70", "80", "100", "120", "150", "200", "250", "350"]
  salary_limits = [limit + "000" for limit in salary_limits]
  salary_limits.append("")
  salary_ranges = [(salary_limits[i], salary_limits[i + 1]) for i in range(len(salary_limits) - 1)]

  # urls with salary ranges
  urls_salary_ranges = []
  for base_url in base_urls:
    for salary_range in salary_ranges:
      # Add salary parameters to url
      urls_salary_ranges.append(base_url + f"?salaryrange={salary_range[0]}-{salary_range[1]}&salarytype=annual")

  # urls with start page
  urls = []  
  for url in urls_salary_ranges:
    # Get max pages per run
    JOBS_PER_PAGE = 22
    SCRAP_PAGES_PER_RUN = 200
    MAX_PAGES_PER_RUN = math.floor(SCRAP_PAGES_PER_RUN/(JOBS_PER_PAGE+1))
    
    # Get number of runs
    number_of_jobs = get_total_jobs_count(url)
    number_of_runs = math.ceil(number_of_jobs/(JOBS_PER_PAGE+1)/MAX_PAGES_PER_RUN)
    
    for run in range(number_of_runs):
      start_page = run * MAX_PAGES_PER_RUN + 1
      # Add page parameter
      urls.append(url + f"&page={start_page}")
    
  return urls


def main():
    gg_sheet_url = 'https://docs.google.com/spreadsheets/d/1lwbfmmsP6N1gNvDrHjPF2CQTsM9nwXIwkjtveXdh37E/edit#gid=1541863908'
    gg_sheet_url = convert_google_sheet_url(gg_sheet_url)
    df = pd.read_csv(gg_sheet_url)
    base_urls = df['URL'].tolist()
    urls = get_urls(base_urls)
    
    number_of_slaves = get_vm_meta_field("number_of_slaves")
    urls_per_slave = len(urls) // number_of_slaves  # Integer division to get floor value

    for i in range(number_of_slaves):
        start_index = i * urls_per_slave
        end_index = start_index + urls_per_slave if i < number_of_slaves - 1 else len(urls)
        urls_for_slave = urls[start_index:end_index]
        
        for url in urls_for_slave:
            run = Run(start_url=url, status="waiting", slave=f"slave{i}", updated=get_current_time())
            db.session.add(run)

    db.session.commit()
if __name__ == "__main__":
    main()