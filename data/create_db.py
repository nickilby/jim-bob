import os
import json
import sqlite3

from jim_bob.search_hostheader import get_data_file_path

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS json_data (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            json_content TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database created and table initialized.")

def load_json_files_to_db(directory_path, db_path):
    if not os.path.isdir(directory_path):
        print(f"Error: The directory {directory_path} does not exist.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    json_file_count = 0  # Initialize counter
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            print(f"Reading file: {file_path}")
            with open(file_path, 'r') as file:
                try:
                    file_data = json.load(file)
                    c.execute('INSERT INTO json_data (filename, json_content) VALUES (?, ?)',
                              (filename, json.dumps(file_data)))
                    print(f"Loaded file: {filename}")
                    json_file_count += 1  # Increment counter
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")
    conn.commit()
    conn.close()
    print(f"All files loaded into the database. Total JSON files evaluated: {json_file_count}")

if __name__ == "__main__":
    directory_path = '/data/platform-config/hosts/vars'
    db_path = get_data_file_path('json_files.db')

    # Create database and load JSON data
    create_database(db_path)
    # load_json_files_to_db(directory_path, db_path)
