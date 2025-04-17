import sqlite3
import requests
import time
import xml.etree.ElementTree as ET

# Connect to the SQLite database (ensure correct path to your DB)
conn = sqlite3.connect('./boardgames.db')
cursor = conn.cursor()

def show_existing_tables():
    """
    Print out the existing tables in the database.
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        print("Existing tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database.")

def populate_game_ids():
    """
    Populate the SQLite database with the most popular game IDs from BoardGameGeek.
    """
    url = 'https://boardgamegeek.com/xmlapi2/hot?type=boardgame'
    
    # Send a request to the BGG API to get the most popular games (by rank)
    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.text))
        root = tree.getroot()

        # Loop through the games and extract IDs and names
        for item in root.findall("item"):
            game_id = item.attrib['id']
            name = item.find("name").attrib['value']
            
            # Insert each game into the database (only if it's not already present)
            cursor.execute('''
                INSERT OR IGNORE INTO games (id, name)
                VALUES (?, ?)
            ''', (game_id, name))
            conn.commit()

            # Print when a new row is added
            print(f"Inserted game ID: {game_id}, Name: {name}")
        
        print("Database population complete!")
    else:
        print("Failed to fetch data from BGG")

# Show existing tables before populating the database
show_existing_tables()

# Call the function to populate the database
populate_game_ids()

# Show the tables again after running the script
show_existing_tables()

# Close the database connection
conn.close()