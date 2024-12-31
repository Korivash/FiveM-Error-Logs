import requests
import subprocess
import datetime
import re
import os
import time

os.system('color 0A')

# Configuration
FIVEM_SERVER_EXECUTABLE_PATH = r""
DISCORD_WEBHOOK_URL = ''

sent_errors = set()

def strip_ansi_escape_codes(text):
    """Remove ANSI escape codes from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def extract_error_details(clean_message):
    """Extract script name and error details from the message."""
    pattern = r'\[\s*(.*?)\]\s*(.*)'
    match = re.search(pattern, clean_message)
    if match:
        return match.group(1), match.group(2)
    parts = clean_message.split(":", 1)
    if len(parts) > 1:
        return parts[0], parts[1]
    return "Unknown Script", clean_message

def send_to_discord(message):
    """Send a developer-friendly embed message to the Discord webhook."""
    global sent_errors
    clean_message = strip_ansi_escape_codes(message)
    if clean_message in sent_errors:
        return

    if len(clean_message) > 1024:
        clean_message = clean_message[:1021] + "..."

    script_name, error_detail = extract_error_details(clean_message)
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getctime(FIVEM_SERVER_EXECUTABLE_PATH))
    embed_color = 0xff0000 if "critical" in error_detail.lower() else 0xffa500 if "warning" in error_detail.lower() else 0xffff00

    data = {
        "embeds": [{
            "title": "FiveM Server Error",
            "description": "An error was detected in the FiveM server console.",
            "color": embed_color,
            "fields": [
                {"name": "Script Name", "value": f"**{script_name}**", "inline": False},
                {"name": "Error Detail", "value": f"```{error_detail.strip()}```", "inline": False},
                {"name": "Server Uptime", "value": f"**{uptime}**", "inline": True}
            ],
            "footer": {"text": "FiveM Error Monitor"},
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")
        print("Response content:", response.text)
    else:
        sent_errors.add(clean_message)

def is_fivem_server_running():
    """Check if the FiveM server process is running."""
    try:
        result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True)
        return FIVEM_SERVER_EXECUTABLE_PATH in result.stdout
    except Exception as e:
        print(f"Error checking server status: {e}")
        return False

def monitor_fivem_server():
    """Monitor the FiveM server console for errors and send them to Discord."""
    while True:
        try:
            process = subprocess.Popen(
                [FIVEM_SERVER_EXECUTABLE_PATH],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(FIVEM_SERVER_EXECUTABLE_PATH),
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )

            for line in iter(process.stdout.readline, ''):
                print(line, end='')
                if "error" in line.lower():
                    send_to_discord(line)

            process.wait()
        except Exception as e:
            print(f"Error starting or monitoring the server: {e}")
        finally:
            time.sleep(10)

if __name__ == "__main__":
    monitor_fivem_server()




