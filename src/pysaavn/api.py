"""Services"""


from requests import Session
from pysaavn.helpers import extract_token, decrypt_media_url
from pysaavn.wrappers import Song, Album, Artist, Playlist


class PySaavn:
    def __init__(self):
        self.session = Session()
        self.domain = "https://www.jiosaavn.com/api.php"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        }
        self.query_calls = {
            "Song": "search.getResults",
            "Album": "search.getAlbumResults",
            "Artist": "search.getArtistResults",
            "Playlist": "search.getPlaylistResults",
        }


    def get_query(self, query, query_type="Song", page=0, no_of_results=20):
        query_uri = f"?p={page}&q={query}&_format=json&_marker=0&api_version=4&ctx=web6dot0&n={no_of_results}&__call={self.query_calls[query_type]}"
        query_url = self.domain + query_uri
        response = self.session.get(query_url, headers=self.headers)
        if response.ok:
            return response.json()

    def parse_query(self, query_json, query_type):
        if query_type == "Song":
            return self.parse_song_query(query_json)
        elif query_type == "Artist":
            return self.parse_artist_query(query_json)
        elif query_type == "Album":
            return self.parse_album_query(query_json)
        elif query_type == "Playlist":
            return self.parse_playlist_query(query_json)
        else:
            pass

    def parse_song_query(self, query_json):
        if isinstance(query_json, dict):
            query_json = query_json["results"]
        songs = []
        for song in query_json:
            song_title = song["title"]
            song_token = extract_token(song["perma_url"])
            song_language = song["language"]
            song_image_url = song["image"]
            song_image_url = song_image_url.replace("-150x150.jpg", "-500x500.jpg")
            song_duration = song["more_info"]["duration"]
            song_album = song["more_info"]["album"]
            song_album_url = song["more_info"]["album_url"]
            song_album_token = extract_token(song_album_url)
            song_media_url = song["more_info"]["encrypted_media_url"]
            song_media_url = decrypt_media_url(song_media_url)
            song_media_url = song_media_url.replace("_96.mp4", "_320.mp4")
            if len(song["more_info"]["artistMap"]["primary_artists"]) != 0:
                song_artist = song["more_info"]["artistMap"]["primary_artists"][0]["name"]
                song_artist_url = song["more_info"]["artistMap"]["primary_artists"][0]["perma_url"]
                song_artist_token = extract_token(song_artist_url)
                song_artist_image = song["more_info"]["artistMap"]["primary_artists"][0]["image"]
            else:
                song_artist = "Unknown"
            song = Song(song_title, song_token, song_language, song_duration, song_media_url, song_image_url,
                        song_album, song_album_token, song_artist, song_artist_token, song_artist_image, song)
            songs.append(song)
        return songs

    def parse_album_query(self, query_json):
        if isinstance(query_json, dict):
            query_json = query_json["results"]
        albums = []
        for album in query_json:
            album_title = album["title"]
            album_url = album["perma_url"]
            album_token = extract_token(album_url)
            album_image_url = album["image"]
            album_song_count = album["more_info"]["song_count"]
            album = Album(album_title, album_token, album_image_url, album_song_count, raw_json=album)
            albums.append(album)
        return albums

    def parse_artist_query(self, query_json):
        if isinstance(query_json, dict):
            query_json = query_json["results"]
        artists = []
        for artist in query_json:
            artist_name = artist["name"]
            artist_url = artist["perma_url"]
            artist_token = extract_token(artist_url)
            artist_image_url = artist["image"]
            artist = Artist(artist_name, artist_token, artist_image_url, raw_json=artist)
            artists.append(artist)
        return artists

    def parse_playlist_query(self, query_json):
        if isinstance(query_json, dict):
            query_json = query_json["results"]
        playlists = []
        for playlist in query_json:
            playlist_title = playlist["title"]
            playlist_url = playlist["perma_url"]
            playlist_token = extract_token(playlist_url)
            playlist_image_url = playlist["image"]
            playlist_song_count = playlist["more_info"]["song_count"]
            playlist_language = playlist["more_info"]["language"]
            playlist = Playlist(playlist_title, playlist_token, playlist_image_url, playlist_song_count, raw_json=playlist)
            playlists.append(playlist)
        return playlists

    def get_album_songs(self, album):
        album_url = f"?__call=webapi.get&token={album.token}&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        album_url = self.domain + album_url
        response = self.session.get(album_url, headers=self.headers)
        raw_json = response.json()
        album.song_list = raw_json["list"]
        album.song_list = self.parse_song_query(album.song_list)
        return album.song_list

    def get_artist_songs(self, artist, page=0, no_of_results=50):
        artist_url = f"?__call=webapi.get&token={artist.token}&type=artist&p={page}&n_song={no_of_results}&n_album={no_of_results}&sub_type=&category=&sort_order=&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        artist_url = self.domain + artist_url
        response = self.session.get(artist_url, headers=self.headers)
        raw_json = response.json() 
        artist.songs = self.parse_song_query(raw_json["topSongs"])
        return artist.songs

    def get_playlist_songs(self, playlist, page=0, no_of_results=50):
        playlist_url = f"?__call=webapi.get&token={playlist.token}&type=playlist&p={page}&n={no_of_results}&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0"
        playlist_url = self.domain + playlist_url
        response = self.session.get(playlist_url, headers=self.headers)
        raw_json = response.json()
        playlist.song_list = raw_json["list"]
        playlist.song_list = self.parse_song_query(playlist.song_list)
        return playlist.song_list


if __name__ == "__main__":
    pass
