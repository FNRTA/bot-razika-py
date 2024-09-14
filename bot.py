import os
import yt_dlp
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from the environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if DISCORD_TOKEN is None:
    raise ValueError("No Discord token found. "
                     "Make sure to set the DISCORD_TOKEN environment variable in your .env file.")


class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.titles_queue = []
        self.currently_playing = None

    @commands.command(name='pl')
    async def play_search(self, ctx, *, song_name: str):

        if len(song_name) > 200:
            print('Too many characters')
            await ctx.send('Too many characters, enter less than 200')

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True
        }

        try:
            # Search for the song
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]

            # Get the video URL and title
            url = info['webpage_url']
            title = info['title']

            # Add to queue
            self.queue.append(url)
            self.titles_queue.append(title)
            print(f"Added to queue: {title}")
            await ctx.send(f"Added to queue: {title}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await ctx.send(f"An error occurred: {str(e)}")
            return

        await self.hanldeVoiceChannel(ctx)


    @commands.command(name='p')
    async def play(self, ctx, *, url):
        # Check if URL is valid
        try:
            if (not url.startswith('https://www.youtube.com/') and
                    not url.startswith('https://youtu.be/')):
                print('Invalid YouTube URL: ', url)
                await ctx.send("Invalid YouTube URL.")
                return

            if "list" in url:
                print('Removing list from url')
                url = url[:url.index("list")]
                print('New url: ', url)

            title = getVideoTitle(url)
            self.titles_queue.append(title)
            self.queue.append(url)
            print(f"Added to queue: {title}")
            await ctx.send(f"Added to queue: {title}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await ctx.send(f"An error occurred: {str(e)}")
            return

        await self.hanldeVoiceChannel(ctx)

    async def hanldeVoiceChannel(self, ctx):
        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.command(name='d', help='Deletes a song from the queue. Usage: !d <song_number>')
    async def delete(self, ctx, song_number: int):
        if not self.queue:
            await ctx.send("The queue is empty.")
            return

        if song_number < 1 or song_number > len(self.queue):
            await ctx.send(f"Invalid song number. Please choose a number between 1 and {len(self.queue)}.")
            return

        index = song_number - 1
        self.queue.pop(index)
        removed_title = self.titles_queue.pop(index)

        await ctx.send(f"Removed from queue: {removed_title}")


    @commands.command(name='q', help='Lists all songs in the queue')
    async def list_queue(self, ctx):
        if not self.titles_queue:
            await ctx.send("The queue is empty.")
        else:
            queue_list = "\n".join([f"{i + 1}. {song_title}" for i, song_title in enumerate(self.titles_queue)])
            await ctx.send(f"Current queue:\n{queue_list}")

    @commands.command(name='s')
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.play_next(ctx)

    @commands.command(name='l')
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    async def play_next(self, ctx):
        if not self.queue:
            await ctx.send("Queue is empty.")
            return

        url = self.queue.pop(0)
        self.titles_queue.pop(0)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -loglevel debug'
        }

        error_extracting = False
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url_from_search = info.get('url', 'NO URL')
        except Exception as e:
            print(f"An error occurred while extracting: {e}")
            error_extracting = True

        if error_extracting and url_from_search == 'NO URL':
            await ctx.send("Error extracting title.")
            return

        ctx.voice_client.play(discord.FFmpegPCMAudio(url_from_search, **ffmpeg_options),
                              after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
        await ctx.send(f"Now playing: {info['title']}")
        print(f"Now playing: {info['title']}")


def getVideoTitle(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown Title')
        except Exception as e:
            print(f"Error extracting title: {e}")
            return 'Unknown Title'


async def setup(bot):
    await bot.add_cog(MusicBot(bot))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await setup(bot)


bot.run(DISCORD_TOKEN)
