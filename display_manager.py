import subprocess


def move_window(app_name, x, y, width, height):
    """
    Uses AppleScript to precisely position an application window.
    MacBook Screen is typically 0,0.
    External Monitor is typically to the right or above.
    """
    script = f'''
    tell application "{app_name}" to activate
    delay 1
    tell application "System Events"
        set b to bounds of window 1 of process "{app_name}"
        set item 1 of b to {x}
        set item 2 of b to {y}
        set item 3 of b to {x + width}
        set item 4 of b to {y + height}
        set bounds of window 1 of process "{app_name}" to b
    end tell
    '''
    subprocess.run(["osascript", "-e", script])


def setup_workspace():
    """
    Sir's specific configuration:
    - MacBook (Main) is on the LEFT (0, 0)
    - External Monitor is on the RIGHT (starts at 1728 or 1920)
    """
    # 1. Launch/Activate Cursor on MacBook Screen
    subprocess.run(["open", "-a", "Cursor"])
    move_window("Cursor", 0, 0, 1400, 900)

    # 2. Launch/Activate Browser for Claude on External Monitor
    # Pushing to the right display.
    subprocess.run(["open", "-a", "Google Chrome", "https://claude.ai"])
    move_window("Google Chrome", 1800, 0, 1920, 1080)

    return "Okay, Sir, opened workspace."


def go_dark():
    """
    Security Protocol: Minimizes all windows and locks the screen.
    """
    script = '''
    tell application "System Events"
        set visible of every process whose visible is true to false
    end tell
    do shell script "open -a ScreenSaverEngine"
    '''
    subprocess.run(["osascript", "-e", script])
    return "Going dark. System secured, Sir."
