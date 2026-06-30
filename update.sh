#!/bin/bash
set -e
cd /home/debian/kjell

git fetch origin master
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
    exit 0
fi

git pull origin master
/home/debian/kjell/bin/pip install -q -r requirements.txt
sudo systemctl restart kjell.service
echo "$(date): updated $LOCAL -> $REMOTE and restarted service"
