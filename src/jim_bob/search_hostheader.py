"""Test with demonstration data."""

from jim_bob import file_finder_service
import json
import sqlite3
import pathlib


def search_hostheader_in_db(target_hostheader, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT json_content FROM json_data")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        data = json.loads(row[0])
        backend_url = search_hostheader_in_dict(data, target_hostheader)
        if backend_url:
            return backend_url
    return None


def search_hostheader_in_dict(data, target_hostheader):
    """Search for a hostheader in a nested dictionary and return the backend_url."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "virtual_hosts" and isinstance(value, list):
                for host in value:
                    if (
                        isinstance(host, dict)
                        and host.get("hostheader") == target_hostheader
                    ):
                        return host.get("backend_url")
            elif isinstance(value, (dict, list)):
                backend_url = search_hostheader_in_dict(value, target_hostheader)
                if backend_url:
                    return backend_url
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                backend_url = search_hostheader_in_dict(item, target_hostheader)
                if backend_url:
                    return backend_url
    return None


def get_data_file_path(filename: str):
    """Get the full path to the data file in the data directory."""
    file_finder = file_finder_service.FileFinderService()
    project_root = file_finder.find_root()
    data_path = pathlib.Path("data")
    data_file = pathlib.Path(filename)
    db_path = project_root / data_path / data_file
    return db_path


if __name__ == "__main__":
    db_path = get_data_file_path("json_files.db")
    target_hostheader = "www.visitbury.com"

    # Search for the hostheader in the database
    backend_url = search_hostheader_in_db(target_hostheader, db_path)
    if backend_url:
        print(f"Backend URL for hostheader '{target_hostheader}' is '{backend_url}'.")
    else:
        print(f"Hostheader '{target_hostheader}' not found in the JSON files.")
