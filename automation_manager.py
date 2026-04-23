import pyautogui
import subprocess

# Safety: move mouse to top-left to abort
pyautogui.FAILSAFE = True


def type_text(text):
    """Types text at the current cursor position."""
    pyautogui.write(text, interval=0.05)
    return "Keystrokes delivered, Sir."


def press_key(key):
    """Presses a specific key (e.g., 'enter', 'space')."""
    pyautogui.press(key)
    return f"{key.capitalize()} key engaged."


def click_at(x, y):
    """Clicks at specific screen coordinates."""
    pyautogui.click(x, y)
    return f"Selection made at coordinate {x}, {y}."


def search_on_screen(image_path):
    """Attempts to find and click an image/icon on screen."""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        if location:
            pyautogui.click(location)
            return "Visual target located and engaged, Sir."
        return "Target not found in visual field."
    except Exception as e:
        return f"Automation error: {str(e)}"


def run_applescript(script):
    """Executes a custom AppleScript for deep app control."""
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return "Script execution complete, Sir."
    except BaseException:
        return "Script execution failed."


def move_mouse_relative(x, y):
    pyautogui.moveRel(x, y, duration=0.25)
    return "Navigation complete."
