from linkedin_jobs_scraper import LinkedinScraper
import csv
from linkedin_jobs_scraper.events import Events
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import (
    RelevanceFilters, TimeFilters, TypeFilters, 
    ExperienceLevelFilters, OnSiteOrRemoteFilters
)
import time
import os
from enum import Enum

def get_enum_input(prompt, enum_cls, default=None):
    while True:
        user_input = input(prompt).strip().upper()
        if not user_input and default is not None:
            return getattr(enum_cls, default, None)
        try:
            return enum_cls[user_input]
        except KeyError:
            print(f"Invalid input. Valid options: {[e.name for e in enum_cls]}")
            if default:
                print(f"Defaulting to {default}.")
                return getattr(enum_cls, default)

job_title = input('Enter job title (default: "software engineer"): ').strip() or "software engineer"
location = input('Enter location (default: "United States"): ').strip() or "United States"

print("\n[Optional Filters - Press Enter to Skip]")
experience_level = input(
    f'Experience level ({[e.name for e in ExperienceLevelFilters]}, default: ANY): '
).strip().upper()
remote_option = input('Remote/on-site (REMOTE, ON_SITE, HYBRID, default: ANY): ').strip().upper()
time_filter = input('Time posted (DAY, WEEK, MONTH, default: MONTH): ').strip().upper()
job_type = input('Job type (FULL_TIME, PART_TIME, CONTRACT, default: FULL_TIME): ').strip().upper()
relevance = input('Relevance (RECENT, RELEVANT, default: RECENT): ').strip().upper()
limit = input('Number of jobs to fetch (default: 20): ').strip()

filters = QueryFilters()

if experience_level:
    filters.experience = [get_enum_input('', ExperienceLevelFilters, default=experience_level)]

if remote_option:
    filters.on_site_or_remote = [get_enum_input('', OnSiteOrRemoteFilters, default=remote_option)]

filters.time = (
    get_enum_input('', TimeFilters, default=time_filter) 
    if time_filter 
    else TimeFilters.MONTH
)

filters.type = [
    get_enum_input('', TypeFilters, default=job_type) 
    if job_type 
    else TypeFilters.FULL_TIME
]

filters.relevance = (
    get_enum_input('', RelevanceFilters, default=relevance) 
    if relevance 
    else RelevanceFilters.RECENT
)

try:
    limit = int(limit) if limit else 20
except ValueError:
    limit = 20

scraper = LinkedinScraper(
    headless=True,  # Run in background (no browser window)
    max_workers=1,  # Reduce detection risk
    slow_mo=2   # Delay between requests
)

query = Query(
    query=job_title,
    options=QueryOptions(
        locations=[location],
        filters=filters,
        limit=limit,
        apply_link=True,
        skip_promoted_jobs=True
    )
)

results = []

def on_data(data):
    results.append([
        data.title,
        data.company,
        data.date,
        data.link,
        data.description[:500] + "..." if data.description else "" 
    ])

scraper.on(Events.DATA, on_data)

try:
    scraper.run([query])
except Exception as e:
    print(f"Scraping failed: {e}")

file_exists = os.path.isfile('linkedin_jobs.csv')

with open('linkedin_jobs.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(['Title', 'Company', 'Date', 'Job Link', 'Description'])
    writer.writerows(results)

print(f"Saved {len(results)} jobs to linkedin_jobs.csv")