import json
import os
import urllib.request
import urllib.error

# GitHub Secret से API Key लें
api_key = os.environ.get("GEMINI_API_KEY")

ai_text = "सफलता का कोई शॉर्टकट नहीं होता, इसके लिए रोज मेहनत करनी पड़ती है।"

if api_key:
    try:
        # सीधे Google Gemini API को बिना किसी भारी लाइब्रेरी के HTTP Request भेजें (यह कभी फेल नहीं होगी)
        url = f"https://generativelanguage.googleapis.com/v1models/gemini-1.5-flash:generateContent?key={api_key}"
        # या gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": "Give one unique, inspiring daily thought in Hindi. Keep it short, within 2 sentences."}]
            }]
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print("API Error:", e)

# content.json फाइल में डेटा सेव करें
new_data = {"text": ai_text}

with open("content.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)

print("Updated successfully with text:", ai_text)
