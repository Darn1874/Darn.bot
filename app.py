from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import os
import requests
from googleapiclient.discovery import build

app = Flask(__name__)

# Database setup
DATABASE = 'whatsapp_bot.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                      id INTEGER PRIMARY KEY,
                      sender TEXT,
                      message TEXT,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# YouTube API setup
YOUTUBE_API_KEY = 'your_youtube_api_key'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_youtube(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return "Sorry, I couldn't find any results."

# Get weather information
def get_weather(location):
    api_key = 'your_openweathermap_api_key'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': location, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        city = data['name']
        country = data['sys']['country']
        return f"Current weather in {city}, {country}: {weather}, {temp}°C"
    else:
        return "Sorry, I couldn't fetch the weather for that location."

# Get a random joke
def get_joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    return f"{joke['setup']} ... {joke['punchline']}"

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')

    # Save message to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", (sender, incoming_msg))
    conn.commit()

    resp = MessagingResponse()

    if incoming_msg.lower() == 'help':
        help_text = (
            "Available commands:\n"
            "1. help - Show this help message\n"
            "2. search <song> - Search and get a YouTube link for the specified song\n"
            "3. weather <location> - Get current weather for the specified location\n"
            "4. joke - Get a random joke\n"
            "5. echo <message> - Repeat back the message"
        )
        msg = resp.message(help_text)
    
    elif incoming_msg.lower().startswith('search'):
        query = ' '.join(incoming_msg.split(' ')[1:])
        video_url = search_youtube(query)
        msg = resp.message(f"Here is the YouTube link: {video_url}")
    
    elif incoming_msg.lower().startswith('weather'):
        location = ' '.join(incoming_msg.split(' ')[1:])
        weather_info = get_weather(location)
        msg = resp.message(weather_info)
    
    elif incoming_msg.lower() == 'joke':
        joke = get_joke()
        msg = resp.message(joke)
    
    elif incoming_msg.lower().startswith('echo'):
        echo_msg = ' '.join(incoming_msg.split(' ')[1:])
        msg = resp.message(echo_msg)
    
    else:
        msg = resp.message("Unknown command. Please use 'help' to see available commands.")

    conn.close()
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
