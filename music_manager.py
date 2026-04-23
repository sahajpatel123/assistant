import subprocess

def control_apple_music(command, playlist=None):
    """
    Orchestrates Apple Music via AppleScript.
    """
    if command == "play":
        if playlist:
            script = f'tell application "Music" to play playlist "{playlist}"'
        else:
            script = 'tell application "Music" to play'
    elif command == "pause":
        script = 'tell application "Music" to pause'
    elif command == "next":
        script = 'tell application "Music" to next track'
    elif command == "previous":
        script = 'tell application "Music" to previous track'
    elif command == "stop":
        script = 'tell application "Music" to stop'
    else:
        return "Invalid music command, Sir."

    subprocess.run(["osascript", "-e", script])
    return f"Apple Music protocol executed: {command}, Sir."

def control_spotify(command, playlist=None):
    """
    Orchestrates Spotify via AppleScript.
    """
    if command == "play":
        if playlist:
            # Note: Spotify AppleScript 'play track' can take a URI
            script = f'tell application "Spotify" to play track "{playlist}"'
        else:
            script = 'tell application "Spotify" to play'
    elif command == "pause":
        script = 'tell application "Spotify" to pause'
    elif command == "next":
        script = 'tell application "Spotify" to next track'
    elif command == "previous":
        script = 'tell application "Spotify" to previous track'
    elif command == "stop":
        script = 'tell application "Spotify" to pause' # Spotify doesn't have 'stop'
    else:
        return "Invalid Spotify command, Sir."

    subprocess.run(["osascript", "-e", script])
    return f"Spotify protocol executed: {command}, Sir."

def set_volume(volume_level):
    """
    Sets system volume (0-100).
    """
    script = f"set volume output volume {volume_level}"
    subprocess.run(["osascript", "-e", script])
    return f"Volume calibrated to {volume_level} percent, Sir."

def get_current_track(player="Music"):
    script = f'tell application "{player}" to get name of current track & " by " & artist of current track'
    try:
        result = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return f"Sir, you are currently listening to {result} on {player}."
    except:
        return f"{player} is currently offline, Sir."
