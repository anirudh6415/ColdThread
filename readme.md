# ColdThread

ColdThread is a Python-based system for automating personalized cold emails to recruiters and professors, complete with templates, scheduling, and follow-up capabilities.

---

## 📁 Project Structure

```
ColdThread/
│
├── .env                          # Contains sender's email credentials (use Gmail App Passwords)
├── main.py                       # Entry point for sending emails
├── logger.py                     # Handles logging of email events
├── readme.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── setup.py                      # Package configuration (if needed)
│
├── data_utils/                   # Utilities for processing input data
│   ├── excel_reader.py           # Reads Excel and CSV files
│   └── generate_email_address.py # Generates email addresses from names
│
├── email_assets/                 # Email content and attachments
│   ├── Anirudh_Resume.pdf
│   ├── Anirudh_Resume_ML.pdf
│   ├── email_template.txt
│   ├── email_template_with_formatting.txt
│   ├── email_template_with_formatting_professors.txt
│   └── follow_up_template.txt
│
├── email_utils/                 # Email management and sending logic
│   ├── email_manager.py         # Manages email flow
│   ├── email_sender.py          # Sends emails using SMTP
│   └── follow_up.py             # Handles follow-up logic
│
├── scheduler/                   # Schedule-based email automation
│   ├── schedule_now.py
│   └── send_later.py
│
├── logs/                        # Email activity logs
│   ├── log_YYYY-MM-DD.log       # Log files per day
│
├── professors.csv               # Contact data for professors
├── recruiters.csv               # Contact data for recruiters
├── recruiters.xlsx              # Optional recruiter Excel file
└── testing.ipynb                # Jupyter notebook for testing utilities
```

---

## 🔧 Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ColdThread.git
   cd ColdThread
   ```

2. **Create and Activate Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env` File:**

   Create a `.env` file in the root directory with the following:
   ```
   EMAIL_ID=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password  # Use an App Password from Gmail
   ```

---

## 🚀 How to Run

To send emails using your input files and selected templates:

```bash
python main.py
```

The script will:
- Read contacts from `professors.csv` or `recruiters.csv`
- Pick the appropriate email template
- Send emails via your Gmail account
- Log the activity into the `logs/` folder

---

## 🛡️ Security Note

This project uses Gmail App Passwords for authentication. Make sure **2FA is enabled** on your Google account and generate an [App Password](https://support.google.com/accounts/answer/185833?hl=en) specifically for this script.

---

## 📌 Future Features

- Email tracking with read receipts
- GUI for managing contacts and templates
- Integration with job boards and research directories
- Automatic classification of responses

---

## 👨‍💻 Author

Anirudh Iyengar  
Machine Learning Intern @ Synapse Labs  
MS in Robotics and AI, Arizona State University

---

## 📝 License

This project is for educational and personal outreach purposes only.