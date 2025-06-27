import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_KEY")

# Function to search real-time insurance policies

def get_policy_recommendations_from_serpapi(user_profile, num_results=5):
    query = f"best insurance policy in India for {user_profile['Age']} year old {user_profile['Occupation']} {user_profile['Gender']} with income {user_profile['Income Level']}"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": num_results
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = []
    for item in data.get("organic_results", [])[:num_results]:
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results