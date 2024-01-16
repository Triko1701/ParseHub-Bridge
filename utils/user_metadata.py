import requests as req
from enum import Enum


HEADER_GG_METADATA = {"Metadata-Flavor": "Google"}
"""
HTTP header for indicating the flavor of metadata when making requests to the Google Cloud Platform (GCP) Metadata Server.
"""

class MetaUrl(Enum):
    """
    Enumeration defining URLs for various Google Cloud Platform (GCP) Metadata Server endpoints.

    Enum Constants:
    - META_PREFIX (str): Base URL prefix for GCP Metadata Server.
    - EXT_IP (str): URL for retrieving the external IP address of the instance.
    - PROJECT_ID (str): URL for retrieving the project ID of the GCP project.
    - ZONE (str): URL for retrieving the zone in which the instance is located.
    - USER_METADATA_PREFIX (str): Base URL prefix for user-defined metadata associated with the instance.
    """
    META_PREFIX = "http://metadata.google.internal/computeMetadata/v1"
    EXT_IP = META_PREFIX + "/instance/network-interfaces/0/access-configs/0/external-ip"
    PROJECT_ID = META_PREFIX + "/project/project-id"
    ZONE = META_PREFIX + "/instance/zone"
    USER_METADATA_PREFIX = META_PREFIX + "/instance/attributes/"


def get_user_metadata(key: str) -> str:
    """
    Retrieve user metadata value for a specified key from Google Cloud Platform (GCP) Metadata Server.

    Parameters:
    - key (str): The key for which the metadata value is requested.

    Returns:
    - str: The value of the user metadata associated with the specified key.

    Raises:
    - requests.exceptions.HTTPError: If the HTTP request to the Metadata Server fails (e.g., if the key is not found).

    Example:
    >>> get_user_metadata('my_custom_key')
    'custom_value'
    """
    r = req.get(MetaUrl.USER_METADATA_PREFIX.value + key, headers=HEADER_GG_METADATA.value)
    r.raise_for_status()    
    return r.text

