"""Models"""


class Song:
    def __init__(self, title, token, language, duration, media_url, image_url, album, album_token, artist, artist_token, artist_image, raw_json):
        self.title = title
        self.token = token
        self.language = language
        self.duration = duration
        self.media_url = media_url
        self.image_url = image_url
        self.album = album
        self.album_token = album_token
        self.artist = artist
        self.artist_token = artist_token
        self.artist_image = artist_image
        self.raw_json = raw_json

    def __str__(self):
        return self.title


class Album:
    def __init__(self, title, token, image_url, song_count, raw_json):
        self.title = title
        self.token = token
        self.image_url = image_url
        self.song_count = song_count
        self.raw_json = raw_json
        self.song_list = []

    def __str__(self):
        return self.title


class Artist:
    def __init__(self, name, token, image_url, raw_json):
        self.name = name
        self.token = token
        self.image_url = image_url
        self.raw_json = raw_json
        self.songs = []

    def __str__(self):
        return self.name


class Playlist:
    def __init__(self, title, token, image_url, song_count, raw_json):
        self.title = title
        self.token = token
        self.image_url = image_url
        self.song_count = song_count
        self.raw_json = raw_json
        self.song_list = []

    def __str__(self):
        return self.title


if __name__ == "__main__":
    pass