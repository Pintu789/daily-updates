import google.generativeai as genai
import json
import os

# यह सीधे आपके GitHub Secrets से सुरक्षित तरीके से API Key ले लेगा
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
  raise ValueError(
      "GEMINI_API_KEY environment variable set nahi ki gayi hai!"
  )

genai.configure(api_key=api_key)

# Gemini मॉडल चुनें
model = genai.GenerativeModel("gemini-1.5-flash")

# एआई के लिए प्रॉम्प्ट
prompt = (
    "Give one unique, inspiring daily thought or interesting fact in Hindi. "
    "Keep it short, meaningful, and within 2-3 sentences."
)

try:
  response = model.generate_content(prompt)
  ai_text = response.text.strip()
except Exception as e:
  ai_text = (
      "आज का नया विचार लोड होने में समस्या आ रही है, जल्द ही अपडेट होगा!"
  )

# JSON डेटा तैयार करें
new_data = {"text": ai_text}

# content.json फाइल में सेव करें
with open("content.json", "w", encoding="utf-8") as f:
  json.dump(new_data, f, ensure_ascii=False, indent=4)

print("Content updated successfully:", ai_text)
