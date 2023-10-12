# FiveM Server Error Monitor

Monitor your FiveM server console for errors and send them directly to a Discord channel using webhooks. This tool helps server administrators get real-time notifications of issues, making debugging and server management more efficient.

## Prerequisites

- Python 3.x installed on the machine where the FiveM server runs.
- `requests` library for Python. Install it using:
  ```bash
  pip install requests


1) Installation
git clone https://github.com/korivash/fivem-error-monitor.git
cd fivem-error-monitor

2) Configuration:
Open the monitor_fivem.py script in a text editor. Modify the following lines:
FIVEM_SERVER_EXECUTABLE_PATH = 'path_to_your_FXServer_executable'
DISCORD_WEBHOOK_URL = 'your_discord_webhook_url'
Replace path_to_your_FXServer_executable with the path to your FiveM server's executable (FXServer.exe). Replace your_discord_webhook_url with the webhook URL from your Discord server.

3) Run the Script:
python monitor_fivem.py

Usage
1)Start the Monitor:
Every time you want to run your FiveM server and monitor it for errors, simply run the monitor_fivem.py script.

2)View Errors in Discord:
When the script detects an error in the FiveM server console, it will send a detailed embed message to the Discord channel associated with the webhook. This embed will contain the error message, a timestamp, and other relevant details.

3)Stop the Monitor:
To stop the monitor, simply press CTRL+C in the terminal where the script is running.