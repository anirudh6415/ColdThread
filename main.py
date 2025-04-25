# main.py
"""
Entry point of ColdContactXLSX.
"""


import email_utils.follow_up as follow_up

from scheduler.schedule_now import send_emails_now
from scheduler.send_later import schedule_emails

# Set up logging
from logger import get_logger
logger = get_logger(__name__)

def main():
    choice = input("Do you wanna mail Professors or Recruiters? (p for Professors, r for Recruiters): ").strip()
    if choice == 'p':
        emailsending_main(professor = True)
    elif choice == 'r':
        emailsending_main(professor = False)
    else:
        print("Invalid choice. Please enter 'p' or 'r'.")

def emailsending_main(professor):
    choice = input("Is this the first email or a follow-up? (1 for first, 2 for follow-up): ").strip()
    if choice == '1':
        first_email_flow(professor)
    elif choice == '2':
        follow_up_flow(professor)
    else:
        print("Invalid choice. Please enter 'first' or 'follow-up'.")

def first_email_flow(professor):
    choice = input("Do you want to send the email now or schedule it? (1 for now, 2 for schedule): ").strip()

    if choice == '1':
        send_emails_now(professor)
    elif choice == '2':
        schedule_emails(professor)
    else:
        print("Invalid choice. Please enter 'now' or 'schedule'.")

def follow_up_flow(professor):
    follow_up.send_follow_up_email(professor)

if __name__ == "__main__":
    main()
