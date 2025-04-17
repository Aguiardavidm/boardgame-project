import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_top_bgg():
    top_games = []
    base_url = "https://boardgamegeek.com/browse/boardgame"
    
    for page in range(1, 6):  # Iterate through first 5 pages (approx. 100 games per page)
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to load page {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.select("tr[id^='row_']")
        for row in rows:
            game_link = row.select_one(".primary")
            if game_link:
                href = game_link["href"]
                bgg_id = int(href.split('/')[2])  # Extract the game ID from the URL
                top_games.append(bgg_id)

        print(f"Fetched {len(top_games)} games so far...")

    print(f"\nTop {len(top_games)} games fetched.")
    return top_games

def insert_game_ids_into_db(game_ids):
    conn = sqlite3.connect("boardgames.db")
    cursor = conn.cursor()

    # Ensure the table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY
        )
    ''')

    # Check how many games already exist
    cursor.execute("SELECT COUNT(*) FROM games")
    existing_count = cursor.fetchone()[0]
    print(f"\n📊 There are currently {existing_count} games in the database.")

    inserted_count = 0
    for game_id in game_ids:
        try:
            cursor.execute("INSERT OR IGNORE INTO games (id) VALUES (?)", (game_id,))
            if cursor.rowcount > 0:
                inserted_count += 1
        except sqlite3.Error as e:
            print(f"SQLite error inserting {game_id}: {e}")
        except Exception as e:
            print(f"Error inserting {game_id}: {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ Done. Inserted {inserted_count} new game IDs.")

if __name__ == "__main__":
    top_game_ids = scrape_top_bgg()
    insert_game_ids_into_db(top_game_ids)
