import subprocess


def trigger_home_scene(scene_name):
    """
    Triggers a HomeKit scene using AppleScript.
    Requires the scene to be defined in the Home app.
    """
    script = f'tell application "Home" to execute scene "{scene_name}"'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return f"Executing {scene_name} protocol, Sir."
    except BaseException:
        # Fallback: Try via Shortcuts if Home app scriptability is limited
        shortcut_script = f'tell application "Shortcuts Events" to run shortcut "{scene_name}"'
        try:
            subprocess.run(["osascript", "-e", shortcut_script], check=True)
            return f"Executing {scene_name} shortcut, Sir."
        except BaseException:
            return f"I could not find a Home scene or shortcut named {scene_name}, Sir."


def control_light(device_name, state="on"):
    """
    Control a specific HomeKit device.
    Note: Direct device control via AppleScript is limited;
    it's usually better to use Scenes or Shortcuts.
    """
    # This is a placeholder for more advanced control if needed
    return trigger_home_scene(f"Turn {device_name} {state}")
