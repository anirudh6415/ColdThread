# ColdThread

ColdThread is an automated system for sending customized emails to recruiters and professors using structured CSV data.

---

## 📁 Project Structure

- `email_assets/`: Contains email templates and formatting requirements.
- `email_utils/`: Includes `manage.py` and `sender.py` to handle the email sending logic.
- `data_utils/`: Responsible for data loading and preprocessing (CSV/Excel).
- `logs/`: Stores logs generated during email sending.
- `scheduler/`: (If used) Automates and schedules email tasks.
- `main.py`: Entry point for the script execution.
- `recruiters.csv` / `professors.csv`: Contact data to use for cold emails.
- `.env`: Contains your email credentials (use Gmail App Password here).
- `requirements.txt`: Python dependencies.

---

## 🔐 Environment Setup

Before running the script, make sure you set up your `.env` file like so:

EMAIL_ID=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

yaml
Copy
Edit

> **Note:** You must generate an **App Password** via your Google account for this to work. Regular passwords won't be accepted due to Gmail security policies.

---

## 🚀 Running the Script

To start sending emails, simply run:

```bash
python main.py
📌 Notes
Make sure your Gmail account allows sending from third-party applications.

The system will read data from recruiters.csv and professors.csv and send customized emails as defined in the email_assets folder.

