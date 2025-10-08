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

    def _get(self, url):
        """
        Internal method to send GET request to a URL and return JSON data.
        """
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def get_artist(self, search_term):
        search_url = f"{self.base_url}/search?q={search_term}"
        json_data = self._get(search_url)

        hits = json_data.get("response", {}).get("hits", [])
        if not hits:
            return None

        artist_id = hits[0]["result"]["primary_artist"]["id"]
        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_data = self._get(artist_url)

        return artist_data.get("response", {})

    def get_artists(self, search_terms):
        records = []

        for term in search_terms:
            artist_info = self.get_artist(term)
            records.append({
                "search_term": term,
                "artist_name": artist_info.get("name") if artist_info else None,
                "artist_id": artist_info.get("id") if artist_info else None,
                "followers_count": artist_info.get("followers_count") if artist_info else None
            })

        return pd.DataFrame(records)
