#!/bin/bash

# Deploy BombSquad server scripts to AWS EC2

SERVER="ubuntu@ec2-18-224-93-194.us-east-2.compute.amazonaws.com"
KEY="~/.ssh/serverbs.pem"
LOCAL_PATH="/Users/less/Documents/projects/Bombsquad/server-scripts/"
REMOTE_PATH="/home/ubuntu/server-scripts/"

echo "Deploying to server..."

rsync -avz \
  --exclude-from='.rsyncignore' \
  -e "ssh -i $KEY" \
  "$LOCAL_PATH" \
  "$SERVER:$REMOTE_PATH"

if [ $? -eq 0 ]; then
    echo "Deploy completed successfully!"
else
    echo "Deploy failed!"
    exit 1
fi
