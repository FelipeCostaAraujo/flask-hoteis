import sqlite3

connection = sqlite3.connect('hotelaria.db')

cursor = connection.cursor()

create_tb = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY,nome text, estrelas real,diaria real,cidade text)"
create_hotel = "INSERT INTO hoteis VALUES ('alpha','Alpha Hotel',4.3, 345.30, 'Rio de Janeiro')"
cursor.execute(create_tb)
cursor.execute(create_hotel)

connection.commit()
connection.close()