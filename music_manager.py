import subprocess

def control_music(command, playlist=None):
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
    return f"Music protocol executed: {command}, Sir."

def get_current_track():
    script = 'tell application "Music" to get name of current track & " by " & artist of current track'
    try:
        result = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        return f"Sir, you are currently listening to {result}."
    except:
        return "Music is currently offline, Sir."
