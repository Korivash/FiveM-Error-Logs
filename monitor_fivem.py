import requests
import subprocess
import datetime
import re
import os 

# Change the console color to green text on a black background
os.system('color 0A')

# Configuration
FIVEM_SERVER_EXECUTABLE_PATH = ''
DISCORD_WEBHOOK_URL = ''

def strip_ansi_escape_codes(text):
    """Remove ANSI escape codes from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def send_to_discord(message):
    """Send a developer-friendly embed message to the Discord webhook."""
    clean_message = strip_ansi_escape_codes(message)
    
   
    if len(clean_message) > 1024:
        clean_message = clean_message[:1021] + "..."

  
    parts = clean_message.split(":", 1)
    if len(parts) > 1:
        script_name, error_detail = parts
    else:
        script_name = "Unknown Script"
        error_detail = clean_message

    data = {
        "embeds": [{
            "title": "Error Detected",
            "description": "An error was detected in the FiveM server console.",
            "color": 0xff0000,  # Red color for errors
            "fields": [
                {
                    "name": "Error Detail",
                    "value": f"`{error_detail.strip()}`",
                    "inline": False
                }
            ],
            "footer": {
                "text": "FiveM Error Monitor"
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")
        print("Response content:", response.text)



def monitor_fivem_server():
    """Monitor the FiveM server console for errors and send them to Discord."""
    process = subprocess.Popen(FIVEM_SERVER_EXECUTABLE_PATH, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8', errors='replace')
    for line in iter(process.stdout.readline, ''):
        print(line, end='')  
        if "error" in line.lower():  
            send_to_discord(line)

if __name__ == "__main__":
    monitor_fivem_server()




