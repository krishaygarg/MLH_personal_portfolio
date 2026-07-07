#!/bin/bash

# Kill all existing tmux sessions to stop any running Flask server
tmux kill-server 2>/dev/null || true

# Navigate to the project directory on the VPS
cd /root/MLH_personal_portfolio

# Fetch the latest changes and hard reset to match remote main
git fetch && git reset origin/main --hard

# Activate the virtual environment and install python dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start the Flask server in a new detached tmux session
tmux new-session -d -s flask_server "cd /root/MLH_personal_portfolio && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0"
