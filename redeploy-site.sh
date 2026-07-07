#!/bin/bash

ssh root@138.68.229.206 << 'EOF'
tmux kill-server 2>/dev/null || true
cd /root/MLH_personal_portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new-session -d -s flask_server "cd /root/MLH_personal_portfolio && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0"
EOF
