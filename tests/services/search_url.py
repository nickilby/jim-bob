import json
import sqlite3

def search_url_in_db(target_url, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT json_content FROM json_data')
    rows = c.fetchall()
    conn.close()
    for row in rows:
        data = json.loads(row[0])
        if search_url_in_dict(data, target_url):
            return True
    return False

def search_url_in_dict(data, target_url):
    """Search for a URL in a nested dictionary."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                found = search_url_in_dict(value, target_url)
                if found:
                    return True
            elif isinstance(value, str) and value == target_url:
                return True
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                found = search_url_in_dict(item, target_url)
                if found:
                    return True
            elif isinstance(item, str) and item == target_url:
                return True
    return False

if __name__ == "__main__":
    db_path = 'json_files.db'
    target_url = 'www.bury.gov.uk'

    # Search for the URL in the database
    if search_url_in_db(target_url, db_path):
        print(f"URL '{target_url}' found in the JSON files.")
    else:
        print(f"URL '{target_url}' not found in the JSON files.")
