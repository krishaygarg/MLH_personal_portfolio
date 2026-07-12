#!/bin/bash

ssh root@138.68.229.206 << 'EOF'
cd /root/MLH_personal_portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

systemctl restart myportfolio
EOF

