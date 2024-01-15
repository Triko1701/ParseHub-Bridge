import re


def convert_google_sheet_url(url: str) -> str:
    """
    Convert a Google Sheets URL to a direct link for exporting the sheet as a CSV file.

    Parameters:
    - url (str): The original Google Sheets URL.

    Returns:
    - str: The new URL for exporting the sheet as a CSV file.

    Note:
    This function uses a regular expression to match and capture the necessary part of the input URL.
    It then constructs a new URL for CSV export, including the sheet ID and, if present, the sheet gid.

    Example:
    >>> convert_google_sheet_url('https://docs.google.com/spreadsheets/d/ABC123456789/edit#gid=987654321')
    'https://docs.google.com/spreadsheets/d/ABC123456789/export?gid=987654321&format=csv'
    """
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url
