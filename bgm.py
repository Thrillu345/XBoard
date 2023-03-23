import vlc

# path to the music file in the Music folder
path = "Music/music.mp3"

# creating a vlc instance
instance = vlc.Instance('--no-xlib')

# creating a media player object
player = instance.media_player_new()

# creating a media object
media = instance.media_new(path)

# setting the media to the media player
player.set_media(media)

# starting the playback
player.play()

# waiting for the playback to finish
while True:
    if player.get_state() == vlc.State.Ended:
        # setting the media to the media player
        player.set_media(media)

        # starting the playback
        player.play()
