# Jarvis Bot

Jarvis Bot is a voice-activated assistant built using Python. The bot can perform various tasks such as telling the time, searching for products on Amazon, launching applications, and learning from user input to improve its responses over time.

## Table of Contents
- [Features](#features)
- [Usage](#usage)
- [Structure](#structure)
- [License](#license)

## Features
- **Voice Interaction:** Communicate with Jarvis using voice commands in Italian.
- **Amazon Search:** Ask Jarvis to search for products on Amazon.
- **Time Queries:** Ask Jarvis for the current time.
- **Launch Applications:** Command Jarvis to open specific applications like Genshin Impact.
- **Machine Learning:** Jarvis uses a machine learning model to improve its responses based on past interactions.
- **Memory and Learning:** Jarvis can learn new responses if it doesn't know how to answer a question, storing new data for future interactions.

## Usage
1. **Start Jarvis Bot:**
    Run the main script:
    ```bash
    python jarvis_bot.py
    ```

2. **Interaction:**
    - Say "Jarvis" to activate the bot.
    - Once activated, you can ask questions, give commands, or teach new responses.
    - To exit the bot, say "Esci".

## Structure
The main components of the project include:

- `jarvis_bot.py`: The main script to run the bot.
- `programmi_appoggio/amazon_scraping.py`: A script for performing Amazon searches.
- `memoria/memoria.json`: JSON file where all learned questions and responses are stored.
- `requirements.txt`: A list of required Python packages.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
