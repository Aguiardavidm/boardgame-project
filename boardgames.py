import sqlite3
import requests
import time
import xml.etree.ElementTree as ET

# Connect to SQLite database
conn = sqlite3.connect('boardgames.db')
cursor = conn.cursor()

def get_bgg_data(game_id):
    """
    Fetch game data from BGG using the BGG API.
    """
    url = f'https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.text)
        
        # Extract relevant data from the XML response
        name = root.find(".//name").attrib.get("value", "Unknown")  # Extract name
        rating = None
        min_players = None
        max_players = None
        year_published = None

        # Extract rating from the statistics section (if available)
        statistics = root.find(".//statistics")
        if statistics is not None:
            rating_element = statistics.find(".//rating")
            if rating_element is not None:
                rating = float(rating_element.attrib.get("value", "0.0"))
        
        # Extract min and max players (if available)
        min_players_element = root.find(".//minplayers")
        if min_players_element is not None:
            min_players = int(min_players_element.attrib.get("value", "1"))
        
        max_players_element = root.find(".//maxplayers")
        if max_players_element is not None:
            max_players = int(max_players_element.attrib.get("value", "1"))
        
        # Extract year published (if available)
        year_published_element = root.find(".//yearpublished")
        if year_published_element is not None:
            year_published = int(year_published_element.attrib.get("value", "0"))
        
        return (game_id, name, rating, min_players, max_players, year_published)
    else:
        print(f"Failed to fetch data for game ID {game_id}")
        return None

def update_game_data():
    """
    Loop through all game IDs in the database, fetch data from BGG, and update the database.
    """
    cursor.execute("SELECT id FROM games")
    game_ids = cursor.fetchall()
    
    for game_id_tuple in game_ids:
        game_id = game_id_tuple[0]
        print(f"Updating game with ID: {game_id}")
        
        # Get the game data from BGG
        game_data = get_bgg_data(game_id)
        
        if game_data:
            # Update the game data in the database
            cursor.execute(''' 
                UPDATE games
                SET name = ?, rating = ?, min_players = ?, max_players = ?, year_published = ?
                WHERE id = ?
            ''', game_data[1:] + (game_data[0],))
            conn.commit()
            print(f"Updated game ID {game_id} with data: {game_data[1:]}")
        
        # Wait 10 seconds before making another request to BGG
        time.sleep(10)

# Run the update function
update_game_data()

# Close the database connection
conn.close()