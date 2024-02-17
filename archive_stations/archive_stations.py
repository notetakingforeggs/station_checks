import sqlite3
from datetime import datetime

def create_table(cursor, table_name):   
    cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    foreign_id INTEGER,
                    city TEXT,
                    station_id INTEGER,
                    name TEXT,
                    latitude REAL,
                    longitude REAL,
                    last_checked TEXT,
                    days_since INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
    conn.commit()

def populate_table(cursor, table_name):
    cursor.execute(f'''
                    INSERT INTO {table_name}(
                    foreign_id,
                    city,
                    station_id,
                    name,
                    latitude,
                    longitude,
                    last_checked,
                    days_since
                    )
                    SELECT 
                    id,
                    city,
                    station_id,
                    name,
                    latitude,
                    longitude,
                    last_checked,
                    days_since
                    FROM stations
             ''')
    conn.commit()

conn = sqlite3.connect("../whatsapp_scraper/stations.db")
cursor = conn.cursor()
table_name = "historical_station_checks_data"

create_table(cursor, table_name)
populate_table(cursor, table_name)