import requests
import subprocess
import datetime

# Configuration
FIVEM_SERVER_EXECUTABLE_PATH = ''
DISCORD_WEBHOOK_URL = ''

import datetime

def send_to_discord(message):
    """Send a developer-friendly embed message to the Discord webhook."""
  
    if len(message) > 2048:
        message = message[:2045] + "..."

    
    if ":" in message:
        script_name = message.split(":", 1)[0]
        message = f"**{script_name}:** {message[len(script_name)+1:]}"

    
    formatted_message = f"```{message}```"

    data = {
        "embeds": [{
            "title": "FiveM Server Error",
            "description": formatted_message,
            "color": 0xff0000,  # Red color for errors
            "fields": [
                {
                    "name": "Error Logs",
                    "value": "servername",  # Replace with your server name or identifier
                    "inline": True
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




