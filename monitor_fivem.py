import requests
import subprocess
import datetime
import re
import os  


os.system('color 0A')

# Configuration
FIVEM_SERVER_EXECUTABLE_PATH = ''
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

    
    if "critical" in error_detail.lower():
        embed_color = 0xff0000  # Critical: Red
    elif "warning" in error_detail.lower():
        embed_color = 0xffa500  # Warning: Orange
    else:
        embed_color = 0xffff00  # General: Yellow

    data = {
        "embeds": [{
            "title": f"**Error in {script_name}**",  # Bold the title
            "description": "An error was detected in the FiveM server console.",
            "color": embed_color,  # Color based on error type
            "fields": [
                {
                    "name": "Error Detail",  
                    "value": f"```{error_detail.strip()}```",  
                    "inline": False
                },
                {
                    "name": "Server Uptime",  
                    "value": f"**{uptime}**",  # Bold the uptime value
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
    else:
        
        sent_errors.add(clean_message)

def monitor_fivem_server():
    """Monitor the FiveM server console for errors and send them to Discord."""
    process = subprocess.Popen(FIVEM_SERVER_EXECUTABLE_PATH, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8', errors='replace')
    for line in iter(process.stdout.readline, ''):
        print(line, end='')  
        if "error" in line.lower(): 
            send_to_discord(line)

if __name__ == "__main__":
    monitor_fivem_server()




