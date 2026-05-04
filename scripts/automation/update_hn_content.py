import json
import urllib.request
import urllib.error
import os
import sys
from datetime import datetime

# Configuration
API_URL = "https://news.ysimulator.run/api/posts?page=1&limit=30"
OUTPUT_FILE = "data/content/hacker-news-posts.json"

def fetch_data():
    print(f"Fetching data from {API_URL}...")
    try:
        # Add User-Agent to avoid being blocked
        req = urllib.request.Request(
            API_URL, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; LocalFirstTools/1.0; +https://github.com/m365-agents-for-python/localFirstTools)'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

def save_data(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Add a metadata field for when this was updated
    if isinstance(data, dict):
        data['_meta'] = {
            'last_updated': datetime.utcnow().isoformat() + 'Z',
            'source': 'news.ysimulator.run'
        }
    
    print(f"Saving data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Success!")

if __name__ == "__main__":
    data = fetch_data()
    save_data(data)
