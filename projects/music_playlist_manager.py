# Dictionary to store playlists
playlists = {}

# Function to create a new playlist
def create_playlist(playlist_name):
    if playlist_name in playlists:
        print(f"Playlist '{playlist_name}' already exists.")
    else:
        playlists[playlist_name] = []  # Initialize an empty list for songs
        print(f"Playlist '{playlist_name}' created.")

# Function to add a song to a playlist
def add_song(playlist_name, song_details):
    if playlist_name not in playlists:
        print(f"Playlist '{playlist_name}' does not exist.")
        return
    playlists[playlist_name].append(song_details)
    print(f"Song '{song_details['title']}' added to '{playlist_name}'.")

# Function to view the songs in a playlist
def view_playlist(playlist_name):
    if playlist_name not in playlists:
        print(f"Playlist '{playlist_name}' does not exist.")
        return
    print(f"Playlist '{playlist_name}':")
    for song in playlists[playlist_name]:
        print(f"- {song['title']} by {song['artist']}")

# Function to list all playlists
def list_playlists():
    if not playlists:
        print("No playlists found.")
        return
    print("Playlists:")
    for playlist_name in playlists:
        print(f"- {playlist_name}")

# Example usage
if __name__ == "__main__":
    while True:
        print("\nMusic Playlist Manager")
        print("1. Create Playlist")
        print("2. Add Song to Playlist")
        print("3. View Playlist")
        print("4. List All Playlists")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the playlist name: ")
            create_playlist(name)
        elif choice == "2":
            name = input("Enter the playlist name: ")
            title = input("Enter the song title: ")
            artist = input("Enter the artist name: ")
            add_song(name, {"title": title, "artist": artist})
        elif choice == "3":
            name = input("Enter the playlist name: ")
            view_playlist(name)
        elif choice == "4":
            list_playlists()
        elif choice == "5":
            print("Exiting Music Playlist Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")




