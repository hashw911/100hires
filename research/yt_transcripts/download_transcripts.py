import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

print("Script is starting! Please wait...")

video_urls = [
    "https://www.youtube.com/watch?v=_b_cTpLHMTM", 
    "https://www.youtube.com/watch?v=8KVqebVRXe8",
    "https://www.youtube.com/watch?v=Hy4eBvxvVfk",
    "https://www.youtube.com/watch?v=GNR61V6ihxE&t=1s",
    "https://www.youtube.com/watch?v=2tgEvv9Irrc"
]

output_folder = os.path.join("research", "youtube-transcripts")
os.makedirs(output_folder, exist_ok=True)
print(f"📁 Ensuring folder exists at: {output_folder}")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

api = YouTubeTranscriptApi()

for url in video_urls:
    print(f"\n🔍 Checking link: {url}")
    video_id = extract_video_id(url)
    
    if not video_id:
        print(f"⚠️ SKIPPED: Could not find a video ID.")
        continue
    
    try:
        print(f"⏳ Downloading transcript for video ID: {video_id}...")
        
        raw_transcript = api.fetch(video_id)
        
        # THE FIX: using item.text instead of item['text']
        clean_text = " ".join([item.text for item in raw_transcript])
        
        file_path = os.path.join(output_folder, f"transcript_{video_id}.txt")
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(clean_text)
        print(f"✅ SUCCESS: Saved to {file_path}")
        
    except Exception as e:
        print(f"❌ FAILED for {video_id}. Reason: {e}")

print("\n🎉 Script is completely finished!")