# scheduler/email_scheduler.py

"""
Module for managing email-related operations such as loading email settings, reading email templates,
and reading data from Excel files.
"""

import os
from dotenv import load_dotenv
from data_utils.excel_reader import read_data_from_excel
from data_utils.generate_email_address import generate_email_address
import pandas as pd

from logger import get_logger
logger = get_logger(__name__)

def load_email_settings():
    """
    Loads email settings from environment variables.

    Returns:
        tuple: Tuple containing email username and password.
    """
    load_dotenv()
    logger.info("Loaded environment variables from .env file.")
    return os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD')

def read_email_template(professor = False):
    """
    Reads the email template from a file.

    Returns:
        str: Email template.
    """
    if professor :
        file_name = 'email_assets/email_template_with_formatting_professors.txt'
    else :
        file_name = 'email_assets/email_template_with_formatting.txt'
    with open(file_name, 'r', encoding='utf-8') as file:
        email_template = file.read()
    logger.info("Read email template.")
    return email_template

def read_follow_up_template(professor = False):
    """
    Reads the follow-up email template from a file.

    Returns:
        str: Follow-up email template.
    """
    if professor :
        file_name = 'email_assets/follow_up_template_professors.txt'
    else :
        file_name = 'email_assets/follow_up_template.txt'
    with open(file_name, 'r') as file:
        follow_up_template = file.read()
    logger.info("Read follow-up email template.")
    return follow_up_template

def read_excel_data():
    """
    Reads data from an Excel file.

    Returns:
        list: List of tuples containing data read from the Excel file.
    """
    excel_file = 'recruiters.xlsx'
    sheet_name = 'Sheet1'
    logger.info(f"Reading data from Excel file: '{excel_file}', sheet: '{sheet_name}'")
    return read_data_from_excel(excel_file, sheet_name)



def read_csv_data(professor = False):
    """
    Reads data from a CSV file.

    Returns:
        list: List of tuples containing data read from the CSV file.
    """
    if professor :
        csv_file = 'professors.csv'
    else :
        csv_file = 'recruiters.csv'
    logger.info(f"Reading data from CSV file: '{csv_file}'")
    return pd.read_csv(csv_file, dtype=str)

def save_csv_data(data, professor):
    """
    Saves data to a CSV file.

    Args:
        data (list of tuples or list of dicts): Data to be saved.
        filename (str): Name of the CSV file.

    Returns:
        None
    """
    if professor :
        filename = 'professors.csv'
    else :
        filename = 'recruiters.csv'
        # Check if data is empty
    if isinstance(data, pd.DataFrame):
        if data.empty:
            logger.info("No data to save.")
            return
        df = data  # Use data directly if it's already a DataFrame

    elif isinstance(data, list):
        if not data:  # Check for an empty list
            logger.info("No data to save.")
            return
        
        # Check if data consists of tuples (assume first row is headers)
        if isinstance(data[0], tuple):
            df = pd.DataFrame(data, columns=["First Name", "Last Name", "Email", "Company Name", "Designation", "Position"])
        else:
            df = pd.DataFrame(data)  # If it's a list of dicts, directly convert
    
    else:
        logger.info("Unsupported data format. Provide a DataFrame or a list of dictionaries/tuples.")
        return

    # Save DataFrame to CSV
    df.to_csv(filename, index=False)
    logger.info(f"Data successfully saved to {filename}")
