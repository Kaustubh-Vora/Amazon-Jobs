# main.py

import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# ========== CONFIG ==========
AMAZON_URL = "https://amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi&radius=24km&industry_experience=one_to_three_years&latitude=&longitude=&loc_group_id=&loc_query=&base_query=Data%20Science&city=&country=&region=&county=&query_options=&"
SEEN_JOBS_FILE = "seen_jobs.json"
EMAIL_SENDER = "ksvora1301@gmail.com"      # <- change this
EMAIL_PASSWORD = "zizu jiup wanq syph"       # <- use App Password if Gmail
EMAIL_RECEIVER = "kaustubh216@gmail.com"    # <- change this
# ============================


def fetch_jobs():
    response = requests.get(AMAZON_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.select(".job-tile")

    jobs = []
    for card in job_cards:
        title = card.select_one(".job-title").get_text(strip=True)
        location = card.select_one(".location-and-id").get_text(strip=True)
        link = "https://www.amazon.jobs" + card.a["href"]
        jobs.append({
            "title": title,
            "location": location,
            "link": link
        })
    return jobs

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_jobs(links):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(list(links), f)

def send_email(new_jobs):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📢 New Amazon Data Science Jobs"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    text_body = "\n\n".join(f"{job['title']} - {job['location']}\n{job['link']}" for job in new_jobs)
    msg.attach(MIMEText(text_body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

def job_runner():
    print("🔍 Checking for new jobs...")
    seen = load_seen_jobs()
    jobs = fetch_jobs()
    new_jobs = [job for job in jobs if job['link'] not in seen]

    if new_jobs:
        print(f"✅ Found {len(new_jobs)} new jobs. Sending notification...")
        send_email(new_jobs)
        seen.update(job["link"] for job in new_jobs)
        save_seen_jobs(seen)
    else:
        print("No new jobs found.")

# Run every hour
schedule.every(10).seconds.do(job_runner)

print("⏳ Job monitor running... (checks every hour)")
while True:
    schedule.run_pending()
    time.sleep(60)
