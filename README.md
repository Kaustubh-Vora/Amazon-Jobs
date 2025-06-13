# Amazon-Jobs

# 🧠 Amazon Data Science Job Alert Bot

Automatically checks [Amazon.jobs](https://www.amazon.jobs/) every hour for new **Data Science** job postings and sends an email notification when new jobs are found.

## 🚀 Features

- Scrapes Amazon.jobs for new Data Science jobs
- Tracks previously seen jobs to avoid duplicate alerts
- Sends email notifications (via Gmail SMTP)
- Runs automatically every hour

## 🛠 Requirements

- Python 3.7+
- Gmail account with App Password enabled
- Dependencies listed in `requirements.txt`

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Kaustubh-Vora/amazon-jobs.git
   cd amazon-jobs

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "your_email@gmail.com"

pip install -r requirements.txt

Test Mode
For fast testing, change in main.py:
schedule.every(10).seconds.do(job_runner)  # TEMPORARY

Then revert to:
schedule.every().hour.do(job_runner)