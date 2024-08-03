# WhatsApp Bot

This is a WhatsApp bot built using Flask and Twilio that provides various features such as searching for music on YouTube, getting current weather information, telling jokes, and echoing messages back to the user.

## Features

- `help`: Show available commands.
- `search <song>`: Search and get a YouTube link for the specified song.
- `weather <location>`: Get current weather for the specified location.
- `joke`: Get a random joke.
- `echo <message>`: Repeat back the message.

## Requirements

- Python 3.8 or higher
- Flask
- Twilio
- Requests
- Google API Python Client

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/whatsapp-bot.git
    cd whatsapp-bot
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Obtain your API keys and update the `app.py` file:
    - [OpenWeatherMap API Key](https://openweathermap.org/api)
    - [YouTube Data API Key](https://developers.google.com/youtube/v3/getting-started)

4. Run the application:

    ```sh
    python app.py
    ```

5. Use [ngrok](https://ngrok.com/) to expose your local server:

    ```sh
    ngrok http 5000
    ```

6. Set the Twilio webhook to the URL provided by ngrok (e.g., `http://your-ngrok-url.ngrok.io/whatsapp`).

## Deployment

To deploy the bot to Heroku:

1. Create a new Heroku app:

    ```sh
    heroku create your-app-name
    ```

2. Deploy your code:

    ```sh
    git add .
    git commit -m "Initial commit"
    heroku git:remote -a your-app-name
    git push heroku master
    ```

3. Set the Twilio webhook to the Heroku app URL (e.g., `https://your-app-name.herokuapp.com/whatsapp`).

## License

This project is licensed under the MIT License.
