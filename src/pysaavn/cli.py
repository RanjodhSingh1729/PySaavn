"""Interface"""

import wget
from InquirerPy import inquirer
from pysaavn.api import PySaavn


App = PySaavn()


def main():
    query = inquirer.text(message="Enter Your Search Keywords:-").execute()
    no_of_results = inquirer.text(message="Enter The Number of Results:-").execute()
    query_type = select("Select Your Search Type:-", ["Song", "Artist", "Album", "Playlist"], multiselect=False)

    query_json = App.get_query(query, query_type=query_type, no_of_results=no_of_results)
    result_list = App.parse_query(query_json, query_type=query_type)
    selected_list = select(f"Select Your {query_type}(s):-", result_list)

    if query_type == "Song":
        download(selected_list)
    if query_type == "Artist":
        complete_selected_list = select_batch(selected_list, App.get_artist_songs)
        download(complete_selected_list)
    elif query_type == "Album":
        complete_selected_list = select_batch(selected_list, App.get_album_songs)
        download(complete_selected_list)
    elif query_type == "Playlist":
        complete_selected_list = select_batch(selected_list, App.get_playlist_songs)
        download(complete_selected_list)
    else:
        pass


def select(message, choices, multiselect=True):
    selected_list = inquirer.select(message=message, choices=choices, multiselect=multiselect, default=None).execute()
    return selected_list


def select_batch(collections, get_songs_method):
    complete_songs_list = []
    for collection in collections:
        current_songs_list = get_songs_method(collection)
        selected_songs_list = select("Select Your Song(s):-", current_songs_list)
        complete_songs_list += selected_songs_list
    return complete_songs_list


def download(song_list):
    for song in song_list:
        url = song.media_url
        out = f"{song}.m4a"
        print(f"\n >>>Dowloading {song}")
        wget.download(url=url, out=out)
        print(f"\n >>>Downloaded {song}")


if __name__ == "__main__":
    main()
