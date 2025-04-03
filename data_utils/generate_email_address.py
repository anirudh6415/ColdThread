# data_utils/generate_email_address.py
"""
Module to generate email addresses based on provided data.
"""


from logger import get_logger
logger = get_logger(__name__)
import pandas as pd 
# Set up logging

def clean_email(email):
    """
    Cleans the email field by handling NaN values and empty strings.

    Args:
        email (str or float): The email value from the CSV.

    Returns:
        str or None: A cleaned email string or None if invalid.
    """
    if isinstance(email, float) and pd.isna(email):  # Handle NaN values
        logger.warning("Email field contains NaN, replacing with None.")
        return None
    elif isinstance(email, str):
        email = email.strip()
        if email == "":  # Handle empty strings
            logger.warning("Email field is empty, replacing with None.")
            return None
        return tuple(e.strip() for e in email.split(",")) if "," in email else email 
    else:
        return email
    
def generate_email_address(first_name, last_name, email, company_name):
    """
    Generates email addresses based on provided data.

    Args:
        first_name (str): First name of the recipient.
        last_name (str): Last name of the recipient.
        email (str): Email address of the recipient.
        company_name (str): Name of the company.

    Returns:
        str or tuple: Generated email address(es).
    """
    logger.info("Generating email addresses...")

    email = clean_email(email)  
    print(email)  
    if email:
        logger.info("Using provided email address.")
        return email
    elif first_name and last_name:
        email1 = f"{first_name.lower()[0]}.{last_name.lower()}@{company_name.lower()}.com"
        email2 = f"{first_name.lower()}.{last_name.lower()[0]}@{company_name.lower()}.com"
        email3 = f"{first_name.lower()}_{last_name.lower()}@{company_name.lower()}.com"
        email4 = f"{first_name.lower()}{last_name.lower()}@{company_name.lower()}.com"
        email5 = f"{first_name.lower()}.{last_name.lower()}@{company_name.lower()}.com"
        logger.info(f"Generated email addresses: '{email1}', '{email2}', '{email3}', '{email4}', '{email5}'.")
        return email1, email2, email3, email4, email5
    elif first_name:
        email = f"{first_name.lower()}@{company_name.lower()}.com"
        logger.info(f"Generated email address: '{email}'.")
        return email
    else:
        logger.warning("Unable to generate email address, insufficient data.")
        return None
