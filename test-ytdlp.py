import yt_dlp
import os
import time

class YouTubeHandler:
    def __init__(self, output_path='./mp3'):
        self.output_path = output_path
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
        }

    def download_audio(self, yt_url):
        start_time = time.time()

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(yt_url, download=False)

                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
                print("Execution time:", round(execution_time), "ms")

                return os.path.join(self.output_path, f"{info['title']}.mp3")
        except Exception as exception:
            print(f"An error occurred: {exception}")
            return None



    def get_stream_url(self, url):
        try:
            with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info['url']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    downloader = YouTubeHandler()
    url = input("Enter a YouTube URL: ")
    # check if url contains list
    try:
        if "list" in url:
            print('list is in url')
            # remove everything after 'list' in the url
            url = url[:url.index("list")]
            print('new url: ', url)
            raise ValueError('exception test')
    except ValueError as e:
        print('Exception caught, exception message: ', e)

    file_path = downloader.download_audio(url)
    if file_path:
        print(f"Audio downloaded successfully: {file_path}")
    else:
        print("Download failed.")

    # Example of how to get stream URL (for Discord bot usage)
    # stream_url = downloader.get_stream_url(url)
    # if stream_url:
    #     print(f"Stream URL: {stream_url}")
    # else:
    #     print("Failed to get stream URL.")
