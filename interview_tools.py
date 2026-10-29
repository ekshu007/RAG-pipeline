import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def search_jobs(role):
    url = "https://jsearch.p.rapidapi.com/search-v2"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": role,
        "page": "1",
        "num_pages": "1"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    descriptions = []

    for job in data["data"]["jobs"]:
        descriptions.append(job["job_description"])

    return "\n\n".join(descriptions)


if __name__ == "__main__":
    descriptions = search_jobs("Data Scientist")
    print(descriptions)