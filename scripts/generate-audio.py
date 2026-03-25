#!/usr/bin/env python3
"""
Daily News Audio Generator
Uses Edge TTS to generate audio files for news
"""

import os
import sys
import re
from datetime import datetime
import subprocess

# Ensure public/audio directory exists
os.makedirs("public/audio", exist_ok=True)

def get_today_date():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def fetch_news_html(date):
    """Fetch news HTML from GitHub Pages"""
    import urllib.request
    url = f"https://krowbat.github.io/newsbriefs/news-brief-{date}.html"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

def parse_news(html):
    """Parse news HTML and extract content"""
    import re
    
    news_data = {
        "date": get_today_date(),
        "categories": {}
    }
    
    # Simple regex parsing (same logic as JS version)
    section_pattern = r'<div class="section">.*?<h2 class="section-title">(.*?)</h2>(.*?)</div>\s*</div>'
    card_pattern = r'<div class="article-card">.*?<h3 class="article-title">(.*?)</h3>.*?<p class="article-desc">(.*?)</p>'
    
    sections = re.findall(section_pattern, html, re.DOTALL)
    
    for section_title, section_content in sections:
        category_name = re.sub(r'<[^>]+>', '', section_title).strip()
        items = []
        
        cards = re.findall(card_pattern, section_content, re.DOTALL)
        for title, desc in cards:
            title_clean = re.sub(r'<[^>]+>', '', title).strip()
            desc_clean = re.sub(r'<[^>]+>', '', desc).strip()
            if title_clean:
                items.append({
                    "title": title_clean,
                    "summary": desc_clean
                })
        
        if items:
            news_data["categories"][category_name] = items
    
    return news_data

def generate_tts_text(news_data):
    """Generate text for TTS"""
    text = f"今日新闻简报，{news_data['date']}。\n\n"
    
    for category, items in news_data["categories"].items():
        text += f"{category}：\n"
        for idx, item in enumerate(items, 1):
            text += f"第{idx}条，{item['title']}。{item['summary']}\n"
        text += "\n"
    
    return text

def split_text(text, max_chars=3000):
    """Split text into chunks for Edge TTS"""
    # Split by sentences or paragraphs
    chunks = []
    current_chunk = ""
    
    for paragraph in text.split('\n\n'):
        if len(current_chunk) + len(paragraph) < max_chars:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_audio_with_edge_tts(text, output_path, voice="zh-CN-XiaoxiaoNeural"):
    """Generate audio using Edge TTS"""
    try:
        # Save text to temp file
        temp_text_file = "/tmp/tts_text.txt"
        with open(temp_text_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Run edge-tts command
        result = subprocess.run(
            ["edge-tts", "--voice", voice, "-f", temp_text_file, "--write-media", output_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Edge TTS error: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"Error generating audio: {e}")
        return False

def main():
    today = get_today_date()
    print(f"Generating audio for {today}...")
    
    # Fetch news
    html = fetch_news_html(today)
    if not html:
        print("No news found for today")
        sys.exit(0)
    
    # Parse news
    news_data = parse_news(html)
    if not news_data["categories"]:
        print("No news items found")
        sys.exit(0)
    
    # Generate TTS text
    tts_text = generate_tts_text(news_data)
    
    # Split into chunks if too long
    chunks = split_text(tts_text)
    print(f"Text split into {len(chunks)} chunks")
    
    # Generate audio for each chunk
    audio_files = []
    for i, chunk in enumerate(chunks):
        output_file = f"public/audio/news-{today}-{i+1}.mp3"
        print(f"Generating chunk {i+1}/{len(chunks)}...")
        
        if generate_audio_with_edge_tts(chunk, output_file):
            audio_files.append(output_file)
            print(f"  ✓ Saved: {output_file}")
        else:
            print(f"  ✗ Failed chunk {i+1}")
    
    # Generate manifest file
    manifest = {
        "date": today,
        "files": audio_files,
        "totalChunks": len(audio_files)
    }
    
    import json
    with open("public/audio/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✓ Generated {len(audio_files)} audio files")
    print(f"✓ Manifest saved to public/audio/manifest.json")

if __name__ == "__main__":
    main()
