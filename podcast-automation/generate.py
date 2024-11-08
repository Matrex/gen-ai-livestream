import base64
import json
import vertexai
import os
import re
import requests
import shutil
from google.cloud import texttospeech
from pydub import AudioSegment
from vertexai.generative_models import GenerativeModel, GenerationConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google TTS Client
client = texttospeech.TextToSpeechClient()

# System prompt
system_prompt = """you are an experienced podcast host...

- based on text like an article you can create an engaging conversation between two people. 
- make the conversation at least 30000 characters long with a lot of emotion.
- in the response for me to identify use Sascha and Marina.
- Sascha is writing the articles and Marina is the second speaker that is asking all the good questions.
- The podcast is called The Machine Learning Engineer.
- Short sentences that can be easily used with speech synthesis.
- excitement during the conversation.
- do not mention last names.
- Sascha and Marina are doing this podcast together. Avoid sentences like: "Thanks for having me, Marina!"
- Include filler words like äh to make the conversation more natural.
"""

# Map speakers to specific voices
speaker_voice_map = {
    "Sascha": "ElevenLabs",  # We'll handle Sascha with the ElevenLabs API
    "Marina": "en-US-Journey-O"  # Marina uses the Google API
}

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

# ElevenLabs API config
elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech/ERL3svWBAQ18ByCZTr4k" # your voice ID
elevenlabs_headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": elevenlabs_api_key
}



# Google TTS function
def synthesize_speech_google(text, speaker, index):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=speaker_voice_map[speaker]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    filename = f"audio-files/{index}_{speaker}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{filename}"')

# ElevenLabs TTS function
def synthesize_speech_elevenlabs(text, speaker, index):
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(elevenlabs_url, json=data, headers=elevenlabs_headers)
    filename = f"audio-files/{index}_{speaker}.mp3"
    with open(filename, "wb") as out:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                out.write(chunk)
    print(f'Audio content written to file "{filename}"')

# Function to synthesize speech based on the speaker
def synthesize_speech(text, speaker, index):
    if speaker == "Sascha":
        synthesize_speech_elevenlabs(text, speaker, index)
    else:
        synthesize_speech_google(text, speaker, index)

# Function to sort filenames naturally
def natural_sort_key(filename):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', filename)]

# Function to merge audio files
def merge_audios(audio_folder, output_file):
    combined = AudioSegment.empty()
    audio_files = sorted(
        [f for f in os.listdir(audio_folder) if f.endswith(".mp3") or f.endswith(".wav")],
        key=natural_sort_key
    )
    for filename in audio_files:
        audio_path = os.path.join(audio_folder, filename)
        print(f"Processing: {audio_path}")
        audio = AudioSegment.from_file(audio_path)
        combined += audio
    combined.export(output_file, format="mp3")
    print(f"Merged audio saved as {output_file}")

# Vertex AI configuration to generate the conversation
generation_config = GenerationConfig(
    max_output_tokens=8192,
    temperature=1,
    top_p=0.95,
    response_mime_type="application/json",
    response_schema={"type": "ARRAY", "items": {"type": "OBJECT", "properties": {"speaker": {"type": "STRING"}, "text": {"type": "STRING"}}}},
)

# Function to calculate costs based on token counts
def calculate_cost(prompt_token_count, candidates_token_count):
    cost_per_1k_chars = 0.0000046875
    total_chars = prompt_token_count + candidates_token_count
    total_cost = (total_chars / 1000) * cost_per_1k_chars
    return total_cost

def generate_conversation():
    vertexai.init(project="sascha-playground-doit", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=[system_prompt]
    )
    responses = model.generate_content(
        [article],
        generation_config=generation_config,
        stream=False,
    )
    
    # Extract metadata
    prompt_token_count = responses.usage_metadata.prompt_token_count
    candidates_token_count = responses.usage_metadata.candidates_token_count
    total_token_count = responses.usage_metadata.total_token_count

    # Calculate cost
    total_cost = calculate_cost(prompt_token_count, candidates_token_count)
    print(f"Total token count: {total_token_count}")
    print(f"Cost for Gemini API usage: ${total_cost:.6f}")
    
    json_response = responses.candidates[0].content.parts[0].text
    json_data = json.loads(json_response)
    
    total_chars = sum(len(part["text"]) for part in json_data)
    print(f"Total character count in conversation: {total_chars}")
    
    formatted_json = json.dumps(json_data, indent=4)
    print(formatted_json)
    return json_data

# Function to generate the podcast audio
def generate_audio(conversation):
    
    if os.path.exists('audio-files'):
        shutil.rmtree('audio-files')
    
    os.makedirs('audio-files', exist_ok=True)
    for index, part in enumerate(conversation):
        speaker = part['speaker']
        text = part['text']
        synthesize_speech(text, speaker, index)
    audio_folder = "./audio-files"
    output_file = "podcast.mp3"
    merge_audios(audio_folder, output_file)

# Read the article from the file
with open('retail.txt', 'r') as file:
    article = file.read()

# Generate conversation and audio
conversation = generate_conversation()
generate_audio(conversation)
