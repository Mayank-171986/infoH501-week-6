# your code here ...
import requests
import pandas as pd

class Genius:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_artist(self, search_term):
        search_url = f"{self.base_url}/search"
        params = {"q": search_term}
        response = requests.get(search_url, headers=self._headers(), params=params)
        response.raise_for_status()
        json_data = response.json()

        hits = json_data.get("response", {}).get("hits", [])
        if not hits:
            return None  # Gracefully handle no results

        primary_artist = hits[0]["result"]["primary_artist"]
        artist_id = primary_artist["id"]

        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self._headers())
        artist_response.raise_for_status()
        artist_data = artist_response.json()

        return artist_data.get("response", {}).get("artist", {})

    def get_artists(self, search_terms):
        records = []

        for term in search_terms:
            artist_info = self.get_artist(term)
            if artist_info:
                records.append({
                    "search_term": term,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count", None)
                })
            else:
                records.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(records)