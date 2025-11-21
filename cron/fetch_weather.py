
#!/usr/bin/env python3
import os
import requests
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Hae API-avain ympäristömuuttujasta
API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITY = 'Herukka'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

# Yhdistä MySQL-tietokantaan
conn = mysql.connector.connect(
    host='localhost',
    user='user',
    password=os.getenv('mysql'),
    database='weather_db'
)
cursor = conn.cursor()

# Luo taulu, jos ei ole olemassa
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    description VARCHAR(100),
    timestamp DATETIME
)
''')

# Hae säädata
response = requests.get(URL)
data = response.json()

# Tarkista, että API-avain toimii
if response.status_code != 200:
    print("Virhe API-haussa:", data)
else:
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    timestamp = datetime.now()

    # Tallenna tietokantaan
    cursor.execute('''
    INSERT INTO weather_data (city, temperature, description, timestamp)
    VALUES (%s, %s, %s, %s)
    ''', (CITY, temp, desc, timestamp))

    conn.commit()
    cursor.close()
    conn.close()

print(f'Data tallennettu: {CITY} {temp}°C {desc}')
