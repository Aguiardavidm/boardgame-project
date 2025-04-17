import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def get_top_bgg_games(pages=5):
    game_ids = []

    for page in range(1, pages + 1):
        url = f"https://boardgamegeek.com/browse/boardgame/page/{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.select("tr[id^='row_']")
        for row in rows:
            title_tag = row.select_one("td.collection_objectname a")
            href = title_tag["href"]

            # Extract the ID using regex from the URL (e.g., /boardgame/174430/gloomhaven)
            match = re.search(r"/boardgame/(\d+)", href)
            if match:
                game_id = int(match.group(1))
                game_ids.append(game_id)

    print(f"\n🔎 Sample IDs: {game_ids[:10]}")
    return game_ids

def insert_game_ids_into_db(game_ids):
    conn = sqlite3.connect("boardgames.db")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY
        )
    """)

    # Show how many games already exist
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
    top_game_ids = get_top_bgg_games(pages=5)
    insert_game_ids_into_db(top_game_ids)