import os


def find_latest_report(directory, prefix):
    """
    Function to find the latest date report with the specified prefix in the given directory.

    Args:
    - prefix (str): Prefix of the report filename.
    - directory (str): Directory path to search for reports.

    Returns:
    - str: Filename of the latest date report with the specified prefix, or None if not found.
    """
    latest_report = None
    latest_creation_time = None

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Check if the file starts with the specified prefix
        if filename.startswith(prefix):
            file_path = os.path.join(directory, filename)
            # Get the creation time of the file
            creation_time = os.path.getctime(file_path)
            # Update latest_report if the file creation time is later than the current latest_creation_time
            if latest_creation_time is None or creation_time > latest_creation_time:
                latest_creation_time = creation_time
                latest_report = filename

    return latest_report
