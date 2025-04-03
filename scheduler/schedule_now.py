# scheduler/schedule_now.py

import time
from data_utils.generate_email_address import generate_email_address
from email_utils.email_sender import send_email
from email_utils.email_manager import load_email_settings, read_email_template,read_csv_data, read_excel_data ,save_csv_data
import pandas as pd

from logger import get_logger
logger = get_logger(__name__)
MAX_RETRIES = 3


def send_emails_now(batch_size=10):
    """
    Sends emails immediately.

    Args:
        batch_size (int): Number of emails to send in each batch.
    """
    sender_email, sender_password = load_email_settings()
    email_template = read_email_template()
    # data = read_excel_data()
    data = read_csv_data()
    if 'message_id'not in data.columns:
        data['message_id'] = ""
    if 'done' not in data.columns:
        data['done'] = ""
    if 'follow_up' not in data.columns:
        data['follow_up'] = ""

    # Split the data into batches
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size]

        for index,row in batch.iterrows():
            if data.loc[index, 'done'] != 'sent':
                retries = 0
                while retries < MAX_RETRIES:
                    # try:
                        first_name, last_name, email, company_name, designation, position,message_id,_,_ = row
                        # print(first_name, last_name, email, company_name, designation, position)
                        if position is None:
                            position = "Machine Learning Engineer/Data Scientist"

                        recipient_emails = generate_email_address(first_name, last_name, email, company_name)
                        # print(recipient_emails)
                        if isinstance(recipient_emails, tuple):
                            for recipient_email in recipient_emails:
                                subject = f"[Anirudh]: Exploring Full-Time {position} Roles at {company_name}"
                                message = email_template.format(first_name=first_name, last_name=last_name, email=recipient_email,
                                                                company_name=company_name,position = position, designation=designation if designation else "esteemed employee")
                                message_id = send_email(sender_email, sender_password, recipient_email, subject, message, company_name,message_id)
                                logger.info(f"Email sent successfully to {recipient_email}")

                                data.loc[index, 'done'] = 'sent'
                                if pd.notna(data.loc[index, 'message_id']) and data.loc[index, 'message_id'].strip() != "":
                                    data.loc[index, 'message_id'] += f", {message_id}"  
                                else:
                                    data.loc[index, 'message_id'] = message_id
                                
                        elif recipient_emails:
                            subject = f"[Anirudh]: Exploring Full-Time {position} at {company_name}"
                            message = email_template.format(first_name=first_name, last_name=last_name, email=recipient_emails,
                                                            company_name=company_name, position = position, designation=designation if designation else "esteemed employee")
                            message_id = send_email(sender_email, sender_password, recipient_emails, subject, message, company_name,message_id)
                            logger.info(f"Email sent successfully to {recipient_emails}")

                            data.loc[index, 'done'] = 'sent'
                            data.loc[index,'message_id'] = message_id
                        # If email sent successfully, break out of the retry loop
                        break
                    # except Exception as e:
                    #     logger.error(f"Error sending email: {e}")
                    #     retries += 1
                    #     logger.info(f"Retrying... Retry attempt {retries}/{MAX_RETRIES}")
                    #     time.sleep(10)  # Wait for a few seconds before retrying

                # If maximum retries reached without success, log error
                if retries == MAX_RETRIES:
                    logger.error("Max retries reached. Unable to send email.")
            else:
                logger.info(f"Skipping {data.loc[index, 'Email']}!!!! already sent ")
    save_csv_data(data)