# your code here ...
import requests
import pandas as pd

#Genious API wrapper class
class Genius:
    def __init__(self, access_token):
        # Save the access token as an instance attribute
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get(self, search_ur):
        # Build the Genius search URL manually
        per_page = 1
        genius_search_url = (
        f"https://api.genius.com/search?q={search_term}&"
        f"access_token={self.access_token}&per_page={per_page}"
        )

        response = requests.get(genius_search_url)
        #response.raise_for_status()
        data = response.json()

        # Ensure 'response' key exists
        if "response" not in data:
            return {"response": {}}

        return data

    def get_artist(self, search_term):

        # Step 1: Read the artist data from the Genius API using the search endpoint
        
        #response = self.get(search_term)
        #response.raise_for_status()

        genius_search_url = (
        f"https://api.genius.com/search?q={search_term}&"
        f"access_token={self.access_token}&per_page={per_page}"
        )

        json_data = self.get(genius_search_url)

        # Step 2: Extract the (most likely, "Primary") Artist ID from the first "hit" of the search_term
        hits = json_data.get("response", {}).get("hits", [])
        if not hits:
            raise ValueError(f"'{search_term}' is not found in Genius database.")

        primary_artist = hits[0]["result"]["primary_artist"]
        artist_id = primary_artist["id"]

        # Step 3: For this Artist ID to pull information about the artist.
        artist_url = f"{self.base_url}/artists/{artist_id}"
        #artist_response = requests.get(artist_url, headers=self._headers())
        #artist_response.raise_for_status()
        artist_data = self.get(artist_url)


        # Step 4: Return the dictionary containing the resulting JSON object.
        return artist_data.get("response", {}).get("artist", {})

    # Step 5: Create a method get_artists that takes a list of search terms and returns a Pandas DataFrame
    def get_artists(self, search_terms):
        artists_data = []

        for item in search_terms:
            #response = self.get(item)
            #response.raise_for_status()
            #artist_info = response.json()
            artist_info = self.get_artist(item)
            if artist_info:
                artists_data.append({
                    "search_term": item,
                    "artist_name": artist_info.get("name"),
                    "artist_id": artist_info.get("id"),
                    "followers_count": artist_info.get("followers_count", None)
                })
            else:
                artists_data.append({
                    "search_term": item,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(artists_data)
    
