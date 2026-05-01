import requests
import urllib.parse
prompt = "Fact-check: Actor Sidharth Venugopal has died? Is it true or false? Start your response with exactly 'TRUE.', 'FALSE.', or 'UNVERIFIABLE.'."
url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
response = requests.get(url, timeout=20).text
print("RESPONSE:", response)
