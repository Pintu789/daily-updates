import json
import os
import urllib.request
from datetime import datetime

# GitHub Secrets से API Key लें
api_key = os.environ.get("GEMINI_API_KEY")

categories = [
    {"slug": "politics", "name": "राजनीति", "query": "latest major Indian political news headlines"},
    {"slug": "tech", "name": "टेक", "query": "latest technology and AI trends news headlines"},
    {"slug": "sports", "name": "खेल", "query": "latest cricket and sports tournament news headlines"},
    {"slug": "business", "name": "व्यापार", "query": "latest stock market and business economy news"},
    {"slug": "entertainment", "name": "मनोरंजन", "query": "latest Bollywood and cinema entertainment news"},
    {"slug": "education", "name": "शिक्षा", "query": "latest education exam and career news in India"},
    {"slug": "lifestyle", "name": "लाइफस्टाइल", "query": "latest lifestyle health and travel trends news"},
    {"slug": "world", "name": "दुनिया", "query": "latest international world news headlines"},
    {"slug": "health", "name": "हेल्थ", "query": "latest health tips and medical science news"},
    {"slug": "auto", "name": "ऑटो", "query": "latest cars bikes vehicle launches news"}
]

new_news_batch = []
id_counter = int(datetime.now().timestamp()) # हर बार यूनिक आईडी बनाने के लिए

if api_key:
    for cat in categories:
        try:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            # एआई से बिल्कुल ताज़ा और विस्तृत जानकारी मांगने के लिए कड़ा निर्देश
            prompt_text = (
                f"Act as a professional news journalist. Provide 3 distinct, fresh, and realistic news items for the category '{cat['name']}' based on recent happenings. "
                "Format each item strictly in this structure:\n"
                "TITLE: [Catchy headline in Hindi]\n"
                "SUMMARY: [Short 2-line summary in Hindi]\n"
                "CONTENT: [Detailed full news article in Hindi with multiple sentences and facts]\n"
                "---"
            )
            data = {
                "contents": [{
                    "parts": [{"text": prompt_text}]
                }]
            }
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                ai_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                
                items = ai_text.split('---')
                for item in items:
                    if "TITLE:" in item and "SUMMARY:" in item:
                        lines = item.strip().split('\n')
                        t, s, c = "", "", ""
                        for line in lines:
                            if line.startswith("TITLE:"):
                                t = line.replace("TITLE:", "").strip()
                            elif line.startswith("SUMMARY:"):
                                s = line.replace("SUMMARY:", "").strip()
                            elif line.startswith("CONTENT:"):
                                c = line.replace("CONTENT:", "").strip()
                        
                        if t and s:
                            new_news_batch.append({
                                "id": id_counter,
                                "category": cat['slug'],
                                "categoryName": cat['name'],
                                "title": t,
                                "summary": s,
                                "content": c if c else s,
                                "image": f"https://picsum.photos/300/200?random={id_counter}",
                                "date": "आज"
                            })
                            id_counter += 1
        except Exception as e:
            print(f"Error for category {cat['name']}: {e}")

# पुरानी फाइलों को पढ़ें और नई खबरों को उसमें जोड़ते जाएं (ताकि खबरें जमा होती रहें और बढ़ती जाएं)
existing_news = []
if os.path.exists("content.json"):
    try:
        with open("content.json", "r", encoding="utf-8") as f:
            existing_news = json.load(f)
    except:
        existing_news = []

# नई खबरों को सबसे आगे जोड़ दें ताकि हमेशा ताज़ा खबरें सबसे ऊपर दिखें
combined_news = new_news_batch + existing_news

# content.json में सेव करें
with open("content.json", "w", encoding="utf-8") as f:
    json.dump(combined_news, f, ensure_ascii=False, indent=4)

print(f"Archo News updated successfully! Total stored news items: {len(combined_news)}")
