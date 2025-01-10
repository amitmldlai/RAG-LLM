from moviepy import VideoFileClip
import os
import yt_dlp
import assemblyai as aai
import glob

from dotenv import load_dotenv
load_dotenv()
cwd = os.getcwd()
data = os.path.join(cwd, "data")
video_path = os.path.join(data, "video", "video.mp4")
image_dir = os.path.join(data, "image")
audio_path = os.path.join(data, "audio", "audio.mp3")
text_path = os.path.join(data, "text", "text.txt")

if not os.path.exists(data):
    os.makedirs(os.path.join(data, "video"))
    os.makedirs(os.path.join(data, "image"))
    os.makedirs(os.path.join(data, "audio"))
    os.makedirs(os.path.join(data, "text"))


def download_video_with_metadata(url):
    """
    Extract metadata from a YouTube video using yt-dlp and download it.

    :param url: URL of the YouTube video
    :return: A dictionary containing author, title, and views
    """
    if not os.path.exists(video_path):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': video_path,
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                if isinstance(info, dict):
                    meta_data = {
                        "Author": info.get('uploader', 'N/A'),
                        "Title": info.get('title', 'N/A'),
                        "Views": info.get('view_count', 'N/A'),
                        "Description": info.get('description', 'N/A'),
                    }
                    print("Download completed successfully!")
                    return meta_data, video_path
                else:
                    print("Error: Unexpected response format.")
                    return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None
    return None, None


def video_to_images():
    """
    Convert a video to a sequence of images and save them to the output folder.

    Parameters:
    video_path (str): The path to the video file.
    output_folder (str): The path to the folder to save the images to.

    """
    if not len(glob.glob(image_dir+'/*.png')):
        clip = VideoFileClip(video_path)
        clip.write_images_sequence(os.path.join(image_dir, "frame%04d.png"), fps=0.1)
    return


def video_to_audio():
    """
    Convert a video to audio and save it to the output path.

    Parameters:
    video_path (str): The path to the video file.
    output_audio_path (str): The path to save the audio to.

    """

    if not os.path.exists(audio_path):
        clip = VideoFileClip(video_path)
        audio = clip.audio
        audio.write_audiofile(audio_path, codec='libmp3lame')
    return


def audio_to_text():
    """
    Convert an audio file to text.

    Parameters:
    audio_path (str): The path to the audio file.

    Returns:
    test (str): The text recognized from the audio.

    """
    if not os.path.exists(audio_path) or not os.path.exists(text_path):
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)
        with open(text_path, "w") as file:
            file.write(transcript.text)
        print("Text data saved to file")
    return


def load_data(video_url):
    video_url = 'https://www.youtube.com/watch?v=GT_Lsj3xj1o'
    download_video_with_metadata(video_url)
    video_to_images()
    video_to_audio()
    audio_to_text()