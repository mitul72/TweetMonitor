# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Discord bot that monitors Twitter/X accounts for new tweets and automatically posts notifications to Discord channels. The bot uses Selenium WebDriver to scrape Twitter content and Discord.py for bot functionality.

## Environment Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env` file:
   - `DISCORD_TOKEN`: Discord bot token
   - `AUTH_TOKEN`: Twitter authentication token for cookie-based login
   - `CT0`: Twitter CSRF token for cookie-based login
   - `EMAIL`: Twitter account email (currently unused)
   - `PASSWORD`: Twitter account password (currently unused)
   - `USER_NAME`: Twitter username (currently unused)

## Running the Bot

- Start the bot: `python src/main.py`
- Test Twitter scraping: `python utils/fetch_tweet_url.py`
- Test login functionality: `python utils/login.py`
- Run test script: `python test.py`

## Architecture

### Core Components

- **`src/main.py`**: Entry point that initializes the Discord bot, loads environment variables, and loads the Twitter cog
- **`src/cogs/twitter_bot.py`**: Main bot logic containing the TwitterCog class that handles tweet monitoring and Discord notifications
- **`utils/login.py`**: Selenium WebDriver setup and Twitter authentication using cookies
- **`utils/fetch_tweet_url.py`**: Tweet scraping logic that fetches the latest tweet URLs from specified Twitter accounts

### Key Features

- **Tweet Monitoring**: Checks for new tweets every 10 minutes using a Discord.py task loop
- **Cookie Authentication**: Uses pre-extracted Twitter auth tokens instead of username/password login
- **Admin Commands**: 
  - `!set_channel`: Set the Discord channel for notifications
  - `!set_role`: Set the role to mention in notifications  
  - `!set_username`: Set the Twitter username to monitor
- **Duplicate Prevention**: Tracks last tweet ID to avoid posting duplicate notifications

### Data Flow

1. Bot initializes Selenium WebDriver with Twitter cookies
2. Every 10 minutes, bot navigates to specified Twitter profile
3. Scrapes latest tweet URL using CSS selectors
4. Compares with stored last tweet ID
5. If new tweet found, posts Discord notification with role mention

## Technical Notes

- Uses Chrome WebDriver with headless options for scraping
- Implements regex pattern matching for tweet URL extraction
- Filters out pinned tweets to avoid false notifications
- Cookie-based authentication bypasses Twitter's login flow
- Nitter configuration present but not actively used in current implementation