# Discord Music Bot

This Discord bot allows users to play music from YouTube in voice channels. It supports basic commands like play, queue, skip, and leave.

## Features

- Play audio from YouTube videos
- Queue system for multiple songs
- Skip current song
- Display current queue
- Leave voice channel

## Requirements

- Python 3.8+
- discord.py library
- yt-dlp library
- FFmpeg

## Installation

1. Install the required Python packages:
   ```
   pip install discord.py yt-dlp
   ```

2. Install FFmpeg:
   - On Ubuntu or Debian: `sudo apt-get install ffmpeg`
   - On macOS using Homebrew: `brew install ffmpeg`
   - On Windows, download from the [official FFmpeg website](https://ffmpeg.org/download.html) and add it to your system PATH.

3. Create a `.env` file in the project root and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

## Usage

1. Run the bot:
   ```
   python bot.py
   ```

2. In Discord, use the following commands:
   - `!p <YouTube URL>`: Play a song or add it to the queue
   - `!pl <song name>`: Will search YouTube a play the first video
   - `!q`: Display the current queue
   - `!s`: Skip the current song
   - `!d <Song number in queue>`: Deletes the song from the queue
   - `!l`: Make the bot leave the voice channel

## Heroku deployment

1. Create Heroku app with the name `discord-bot-razika-py`
2. Login in Heroku cli: 
```
heroku login
```
3. Install ffmpeg:
```
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```
4. Deploy
```
git push heroku main
```

## Development

### Running Tests

To run the unit tests:

```
python -m unittest test_bot.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Support

If you encounter any problems, please file an issue along with a detailed description.


