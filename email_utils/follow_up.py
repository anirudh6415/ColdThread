# email_utils/follow_up.py

"""
Module for sending follow-up emails to recipients.

This module includes functionality to load email settings, read email templates,
read recipient data from an Excel file, and send follow-up emails.

"""

from email_utils.email_sender import send_email
from email_utils.email_manager import load_email_settings, read_email_template, read_csv_data,read_excel_data, read_follow_up_template,save_csv_data
from data_utils.generate_email_address import generate_email_address  # Import the generate_email_address function


from logger import get_logger
logger = get_logger(__name__)

def send_follow_up_email():
    """
    Sends follow-up emails to recipients.

    This function loads email settings, email templates, and recipient data,
    and then iterates through each recipient to send a follow-up email.

    """
    sender_email, sender_password = load_email_settings()
    email_template = read_email_template()
    follow_up_template = read_follow_up_template()
    # data = read_excel_data()
    data = read_csv_data()
    if 'follow_up' not in data.columns:
        data['follow_up'] = ""

    for index,row in data.iterrows():
        if data.loc[index, 'follow_up'] != 'sent':
            first_name, last_name, email, company_name, designation, position,message_id,_,_= row

            generated_emails = generate_email_address(first_name, last_name, email, company_name)
            
            if position is None:
                position = "Machine Learning Engineer/Data Scientist"
            # Iterate through generated email addresses and send follow-up emails
            if isinstance(generated_emails, tuple):
                for email in generated_emails:
                    if email:
                        # print(email)
                        subject = f"Re: Exploring Full-Time {position} Roles at {company_name}"
                        message = follow_up_template.format(first_name=first_name, last_name=last_name, email=email,
                                                        company_name=company_name,position = position,designation=designation if designation else "esteemed employee")
                        # Add additional string after "original email"
                        # original_email_info = f"\n\n--------------- ORIGINAL EMAIL ---------------\n\n" \
                        #                     f"\nFrom: {sender_email}\nTo: {email}\nSubject: [Anirudh]: Exploring Full-Time {position} Roles at {company_name}\n\n"
                        # message += original_email_info
                        # message += email_template.format(first_name=first_name, last_name=last_name, email=email,
                        #                                 company_name=company_name,position = position,designation=designation if designation else "esteemed employee")

                        message_id=send_email(sender_email, sender_password, email, subject, message, company_name,message_id)
                        logger.info(f"follow-up email sent successfully to {email}")

                        data.loc[index, 'follow_up'] = 'sent'
                        data.loc[index,'message_id'] = message_id
                    else:
                        logger.warning("Skipping follow-up email: Unable to generate recipient email address.")
            elif generated_emails:
                email = generated_emails
                subject = f"Re: [Anirudh]: Exploring Full-Time {position} Roles at {company_name}"
                message = follow_up_template.format(first_name=first_name, last_name=last_name, email=email,
                                                company_name=company_name,position = position,designation=designation if designation else "esteemed employee")
                # Add additional string after "original email"
                # original_email_info = f"\n\n--------------- ORIGINAL EMAIL ---------------\n\n" \
                #                     f"\nFrom: {sender_email}\nTo: {email}\nSubject: [Anirudh]: Exploring Full-Time {position} Roles at {company_name}\n\n"
                # message += original_email_info
                # message += email_template.format(first_name=first_name, last_name=last_name, email=email,
                #                                 company_name=company_name,position = position,designation=designation if designation else "esteemed employee")

                message_id =send_email(sender_email, sender_password, email, subject, message, company_name,message_id)
                logger.info(f"follow-up email sent successfully to {email}")

                data.loc[index, 'follow_up'] = 'sent'
                data.loc[index,'message_id'] = message_id
        else:
            logger.info(f"Skipping the follow-up for {data.loc[index, 'Email']}!!!! already sent ")
    save_csv_data(data)