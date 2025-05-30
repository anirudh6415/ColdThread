# email_utils/email_sender.py
"""
Module to handle sending emails.
"""

import os
import smtplib
import time
import pandas as pd
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid



# Set up logging

from logger import get_logger
logger = get_logger(__name__)


def select_resume(position: str) -> str:
    position = position.lower()
    
    if position.startswith("data engineer") or "data engineer" in position:
        role_code = "DE"
    elif position.startswith("analyst") or "analyst" in position:
        role_code = "DA"
    elif position.startswith("data scientist") or "data scientist" in position:
        role_code = "DS"
    elif position.startswith("machine learning") or "machine learning" in position or \
        "artificial intelligence" in position or "ai engineer" in position :
        role_code = "ML"
    elif position.startswith("software") or "software" in position:
        role_code = "Sd"
    else:
        raise ValueError("Position string did not match any known resume types.")
    
    resume_filename = f"Anirudh_Resume_{role_code}.pdf"
    resume_path = os.path.join("email_assets", resume_filename)
    
    return resume_path,resume_filename

def clean_message_id(message_id):
    """
    Cleans the message_id field by handling empty strings and NaN values.

    Args:
        message_id (str or float): The message_id value from the CSV.

    Returns:
        str or None: A cleaned message_id string or None if invalid.
    """
    if isinstance(message_id, float) and pd.isna(message_id):  # Handle NaN values
        logger.warning(f"Message-ID field contains NaN, replacing with None.{message_id}")
        return None
    elif isinstance(message_id, str) and message_id.strip() == "":  # Handle empty strings
        message_id = message_id.strip()
        if message_id == "":
            logger.warning("Message-ID field is empty, replacing with None.")
            return None
        tuple(e.strip() for e in message_id.split(",")) if "," in message_id else message_id
    else:
        return message_id


def send_email(sender_email, sender_password, recipient_email, subject, message, company_name,position,message_id = None):
    """
    Sends an email with an attachment.
    
    Args:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        message (str): Email body message.
        company_name (str): Name of the company.
    """
    logger.info(f"Sending email to: {recipient_email}")
    try:
        original_message_ids = clean_message_id(message_id)
        if isinstance(original_message_ids, tuple):
            allmail_id = ""
            for original_message_id in original_message_ids:
                server =smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.add_header('X-Priority', '3')
                msg.add_header('X-MSMail-Priority', 'Normal')
                msg.add_header('Importance', 'Normal')
                new_message_id = make_msgid(domain='gmail.com')

                msg['Message-ID'] = new_message_id
                if original_message_id:  
                    original_message_id = str(original_message_id).strip()
                    if "@" in original_message_id:
                        logger.info(f"Referencing to message_id: {original_message_id} for {recipient_email}")
                        msg['In-Reply-To'] = original_message_id
                        msg['References'] = original_message_id


                logger.info(f"Using message_id: {message_id} for {recipient_email}")
                # msg.attach(MIMEText(message, 'plain'))
                msg.attach(MIMEText(message, 'html')) #- uncomment if you want your message to be formatted
                

                resume_path,resume_filename = select_resume(position)
                with open(resume_path, 'rb') as file:
                    resume_attachment = MIMEApplication(file.read(), Name=resume_filename)
                resume_attachment['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
                msg.attach(resume_attachment)
                
                server.sendmail(sender_email, recipient_email, msg.as_string())
                logger.info(f"Email sent successfully to {recipient_email}")

                # Log successfully sent email address to a text file
                # success_log_file = f"{company_name}_successfully_sent_emails.txt"
                # with open(success_log_file, 'a') as file:
                #     file.write(recipient_email + '\n')
                server.quit()
                if allmail_id:
                    allmail_id += f", {new_message_id}"
                else:
                    allmail_id = new_message_id
            return allmail_id
        else:
            server =smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.add_header('X-Priority', '3')
            msg.add_header('X-MSMail-Priority', 'Normal')
            msg.add_header('Importance', 'Normal')
            new_message_id = make_msgid(domain='gmail.com')

            msg['Message-ID'] = new_message_id
            if original_message_ids:  
                original_message_ids = str(original_message_ids).strip()
                if "@" in original_message_ids:
                    logger.info(f"Referencing to message_id: {original_message_ids} for {recipient_email}")
                    msg['In-Reply-To'] = original_message_ids
                    msg['References'] = original_message_ids


            logger.info(f"Using message_id: {message_id} for {recipient_email}")
            # msg.attach(MIMEText(message, 'plain'))
            msg.attach(MIMEText(message, 'html')) #- uncomment if you want your message to be formatted
            
            resume_path,resume_filename = select_resume(position)

            with open(resume_path, 'rb') as file:
                resume_attachment = MIMEApplication(file.read(), Name=resume_filename)
            resume_attachment['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
            msg.attach(resume_attachment)
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            logger.info(f"Email sent successfully to {recipient_email}")

            return new_message_id
    except Exception as e:
        logger.error("Error sending email:", exc_info=True)
        raise e
    
    
