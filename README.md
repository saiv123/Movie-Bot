# Movie-Bot

[![Python Tests](https://github.com/your-username/Movie-Bot/actions/workflows/main.yml/badge.svg)](https://github.com/your-username/Movie-Bot/actions/workflows/main.yml)
![Python Version](https://img.shields.io/badge/python-3.10-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributions](https://img.shields.io/badge/contributions-welcome-orange)

A bot for managing movies and TV shows using The Movie Database (TMDb) API.

## Features
- Add movies or TV shows to your watchlist.
- Search for movies or TV shows by name or ID.
- Slash commands and context menu support.

## Setup
1. Clone the repository.
2. Add your `secrets.py` file with your TMDb API key and bot token.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Testing
Run the unit tests:
```bash
python -m unittest discover -s . -p "test*.py"
```
