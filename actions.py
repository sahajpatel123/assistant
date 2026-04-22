import subprocess
import urllib.parse

def speak(text, voice="Samantha"):
    """
    Uses MacOS native 'say' command for zero-latency, offline text-to-speech.
    'Samantha' is a clean, standard US Siri-like voice.
    """
    print(f"Christin: {text}")
    subprocess.run(["say", "-v", voice, text])

def make_call(phone_number):
    """
    Initiates a phone call using Mac's Continuity via your nearby iPhone.
    The tel:// scheme automatically triggers FaceTime to route an audio call.
    """
    url = f"tel://{phone_number}"
    subprocess.run(["open", url])
    return f"Initiating call to {phone_number}."

def send_imessage(contact, message):
    """
    Uses AppleScript to silently send an iMessage/SMS in the background.
    """
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{contact}" of targetService
        send "{message}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    return f"Message sent to {contact}."

def send_whatsapp(phone_number, message):
    """
    Opens WhatsApp desktop (if installed) to send a message.
    """
    encoded_message = urllib.parse.quote(message)
    url = f"whatsapp://send?phone={phone_number}&text={encoded_message}"
    subprocess.run(["open", url])
    return "WhatsApp opened with the message ready."

def open_news_globe():
    """
    Opens our local 3D News Globe widget in the default browser.
    """
    subprocess.run(["open", "http://127.0.0.1:5050/"])
    return "Displaying the global news interface."
