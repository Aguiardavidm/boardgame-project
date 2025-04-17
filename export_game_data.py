import sqlite3
import csv

# Connect to your SQLite DB
conn = sqlite3.connect('boardgames.db')
cursor = conn.cursor()

# Query all data from the games table
cursor.execute("SELECT * FROM games")
rows = cursor.fetchall()

# Get column names from the table
column_names = [description[0] for description in cursor.description]

# Add a new column for the BGG game URL
column_names.append("game_url")

# Open CSV file for writing
with open("games_export.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_names)  # Write the header row

    for row in rows:
        game_id = row[0]
        url = f"https://boardgamegeek.com/boardgame/{game_id}"
        writer.writerow(list(row) + [url])  # Append the URL to each row

# Done!
conn.close()
print("✅ Exported games table to games_export.csv with BGG URLs.")