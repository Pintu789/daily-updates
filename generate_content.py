import json
import os
import urllib.request

# GitHub Secrets से API Key लें
api_key = os.environ.get("GEMINI_API_KEY")

categories = [
    {
        "slug": "politics",
        "name": "राजनीति",
        "prompt": (
            "Write a trending political news headline and brief article in"
            " Hindi."
        ),
    },
    {
        "slug": "tech",
        "name": "टेक",
        "prompt": (
            "Write a trending technology news headline and brief article in"
            " Hindi."
        ),
    },
    {
        "slug": "sports",
        "name": "खेल",
        "prompt": (
            "Write a trending sports news headline and brief article in Hindi."
        ),
    },
    {
        "slug": "business",
        "name": "व्यापार",
        "prompt": (
            "Write a trending business/market news headline and brief article in"
            " Hindi."
        ),
    },
    {
        "slug": "entertainment",
        "name": "मनोरंजन",
        "prompt": (
            "Write a trending entertainment/cinema news headline and brief"
            " article in Hindi."
        ),
    },
]

news_list = []
id_counter = 1

for cat in categories:
  title = f"आज की ताजा {cat['name']} खबर"
  summary = "इस समय की सबसे बड़ी और महत्वपूर्ण खबर यहाँ पढ़ें।"
  content = (
      "यह इस खबर की पूरी विस्तृत जानकारी है जिसे स्वचालित रूप से अपडेट किया"
      " गया है। इसके सभी पहलुओं पर विस्तार से चर्चा की गई है।"
  )

  if api_key:
    try:
      url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
      headers = {"Content-Type": "application/json"}
      data = {
          "contents": [{
              "parts": [{
                  "text": (
                      f"Give a short catchy Hindi headline and a 2-sentence"
                      f" Hindi description for: {cat['prompt']}"
                  )
              }]
          }]
      }
      req = urllib.request.Request(
          url,
          data=json.dumps(data).encode("utf-8"),
          headers=headers,
          method="POST",
      )
      with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        ai_text = (
            res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        )
        lines = ai_text.split("\n")
        if len(lines) > 0:
          title = lines[0].replace("#", "").strip()
        if len(lines) > 1:
          summary = lines[1].strip()
          content = ai_text
    except Exception as e:
      print("API Error for", cat["name"], e)

  news_list.append({
      "id": id_counter,
      "category": cat["slug"],
      "categoryName": cat["name"],
      "title": title,
      "summary": summary,
      "content": content,
      "image": f"https://picsum.photos/300/200?random={id_counter}",
      "date": "आज",
  })
  id_counter += 1

# content.json में सेव करें
with open("content.json", "w", encoding="utf-8") as f:
  json.dump(news_list, f, ensure_ascii=False, indent=4)

print("Archo News content updated successfully!")
