import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("EXPO_PUBLIC_MOVIE_API")

class TmdbClient:
    BASE_URL = 'https://api.themoviedb.org/3'


    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("TMDB API key not found")
        
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
    def _fetch_movie(self, query: str | None):
        if query:
            url = f"{self.BASE_URL}/{query}"
        else:
            url = f"{self.BASE_URL}/discover/movie?sort_by=popularity.desc"

        response = requests.get(url, headers=self.headers, timeout=8)
        data = response.json()

        if response.status_code !=200:
            raise Exception(f"TMDB API error: {response.status_code} - {response.text}")
        
        return data
    

if __name__ == "__main__":
    client = TmdbClient(api_key=api_key)




# url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer"
# }

# response = requests.get(url, headers=headers)

# print(response.text)