import yt_dlp
import whisper
import streamlit as st
import os

from datetime import datetime

model = whisper.load_model("small")

def download_audio(url):
    """
    Downloads audio from a YouTube video as an MP3 file with a unique name.

    Parameters:
    - url (str): The URL of the YouTube video.
    """
    # Generate a unique filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join('audio', f"audio_{timestamp}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Use yt_dlp to download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Audio downloaded as {output_filename}")
    return output_filename

def extract_transcriptions(audio_file):

    result = model.transcribe(audio_file)
    return result['text']

def summary_generation(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']


def generate_summary_from_video(video_path):
    # Step 1: Extract audio
    audio_path = download_audio(video_path)

    # Step 2: Transcribe the audio
    transcript = extract_transcriptions(audio_path+".mp3")


    return transcript


def main():
	# giving the webpage a title
	st.title("Iris Flower Prediction")

	# here we define some of the front end elements of the web page like
	# the font and background color, the padding and the text to be displayed
	html_temp = """
	<div style ="background-color:#E68369;padding:13px ;border-radius:10% ">
	<h2 style ="color:white;text-align:center;">Streamlit Iris Flower Classifier</h2>
	</div><br>
	"""
	st.markdown(html_temp, unsafe_allow_html = True)
	youtube_link = st.text_input("Enter Your Video Link:")
	if youtube_link:
		video_id = youtube_link.split("=")[1]
		print(video_id)
		st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
	
	if st.button("Get Detailed Notes"):
		transcript_text=generate_summary_from_video(youtube_link)
		if transcript_text:
			st.markdown("## Detailed Notes:")
			st.write(transcript_text)
  # this line allows us to display the front end aspects we have
  # defined in the above code


 
      
if __name__=='__main__':
	main()
