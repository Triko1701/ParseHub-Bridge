import time
import math

import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from sqlalchemy import and_, select

from utils import get_user_metadata, convert_google_sheet_url
from .app import create_app
from .app.models import Run, RunStatus, Meta


def get_total_jobs_count(job_search_url: str) -> int:
  time.sleep(0.5)
  response = req.get(job_search_url)
  
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


def remove_existing_base_url(base_urls, db, app):
  with app.app_context(), db.session.begin():
    for base_url in base_urls:
      url_exist = db.session.query(select(1).filter(
            and_(
                Run.start_url.like(f"%{base_url}%"),
                Run.status == RunStatus.WAITING.value
            )
      ).exists()).scalar()
      
      if url_exist:
        base_urls.remove(base_url)


def get_urls(base_urls: list(str)) -> list(str):
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


def main() -> None:
  app = create_app()
  db = app.extensions["sqlalchemy"]  
  
  GG_SHEET_URL = get_user_metadata(Meta.GG_SHEET_URL.value)
  NUM_SLAVES = get_user_metadata(Meta.NUM_SLAVES.value)
  gg_sheet_url = convert_google_sheet_url(GG_SHEET_URL)
  df = pd.read_csv(gg_sheet_url)
  base_urls = df.get('URL').tolist()
  remove_existing_base_url(base_urls, db, app)
  urls = get_urls(base_urls)
  
  URLS_PER_SLAVE = len(urls) // NUM_SLAVES
  with app.app_context(), db.session.begin():
      for i in range(NUM_SLAVES):
          start_index = i * URLS_PER_SLAVE
          end_index = start_index + URLS_PER_SLAVE if i < NUM_SLAVES - 1 else len(urls)
          urls_for_slave = urls[start_index:end_index]
          
          for url in urls_for_slave:
              run = Run(start_url=url, slave=f"slave{i+1}")
              db.session.add(run)

        
if __name__ == "__main__":
    main()
  