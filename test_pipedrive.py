import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("PIPEDRIVE_API_TOKEN")
print(f"Loaded Token: {repr(api_token)}")

if api_token:
    url = f"https://api.pipedrive.com/v1/users?api_token={api_token}"
    try:
        response = requests.get(url)
        print("Response Code:", response.status_code)
        print("Response JSON:", response.json())
    except Exception as e:
        print("❌ Error making request:", e)
else:
    print("❌ API token not loaded. Check .env file.")
