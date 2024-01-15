def get_dict_field(dictionary: dict, target_key: str):
    """
    Recursively search for a specific field with a known key name in a dictionary with unknown structure.

    Args:
    - dictionary (dict): The dictionary to search.
    - target_key (str): The key name to look for.

    Returns:
    - The value associated with the target_key if found, otherwise None.
    """
    if isinstance(dictionary, dict):
        # Check if the target_key is in the current level of the dictionary
        if target_key in dictionary:
            return dictionary[target_key]
        else:
            # If the target_key is not found, recursively search in the values of the dictionary
            for value in dictionary.values():
                result = get_dict_field(value, target_key)
                if result is not None:
                    return result

    # If the dictionary is not a dict or the target_key is not found, return None
    return None