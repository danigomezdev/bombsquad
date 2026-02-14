#!/bin/bash
set -e

# BombSquad Server Deployment Script
# Deploys server to development or production environment
# Usage:
#   ./deploy.sh         - Use .env configuration
#   ./deploy.sh dev     - Quick deploy with dev defaults
#   ./deploy.sh prod    - Quick deploy with prod defaults

echo "======================================="
echo "BombSquad Server Deployment"
echo "======================================="
echo ""

# Check for quick deployment flags
if [ "$1" = "dev" ]; then
    echo "Using DEV preset configuration..."
    ENVIRONMENT="development"
    SERVER_NAME="test"
    PARTY_NAME="Teams @ Less Test"
    PORT="6666"

    # Load SSH config from .env if it exists
    if [ -f ".env" ]; then
        SSH_HOST=$(grep "^SSH_HOST=" .env | cut -d'=' -f2 | tr -d '"')
        SSH_KEY=$(grep "^SSH_KEY=" .env | cut -d'=' -f2 | tr -d '"')
    fi

elif [ "$1" = "prod" ]; then
    echo "Using PROD preset configuration..."
    ENVIRONMENT="production"
    SERVER_NAME="less"
    PARTY_NAME="Teams @ Less East 1"
    PORT="43210"

    # Load SSH config from .env if it exists
    if [ -f ".env" ]; then
        SSH_HOST=$(grep "^SSH_HOST=" .env | cut -d'=' -f2 | tr -d '"')
        SSH_KEY=$(grep "^SSH_KEY=" .env | cut -d'=' -f2 | tr -d '"')
    fi

else
    # Load from .env file
    if [ ! -f ".env" ]; then
        echo "Error: .env file not found!"
        echo "Please copy .env.example to .env and configure it."
        echo ""
        echo "Or use quick deploy:"
        echo "  ./deploy.sh dev   - Deploy with dev defaults"
        echo "  ./deploy.sh prod  - Deploy with prod defaults"
        exit 1
    fi

    echo "Loading configuration from .env..."
    source .env

    # Set defaults if not provided
    PORT=${PORT:-6666}
    PARTY_NAME=${PARTY_NAME:-"BombSquad Server"}
fi

# Validate required variables
if [ -z "$ENVIRONMENT" ] || [ -z "$SERVER_NAME" ] || [ -z "$SSH_HOST" ] || [ -z "$SSH_KEY" ]; then
    echo "Error: Missing required configuration"
    echo "Required: ENVIRONMENT, SERVER_NAME, SSH_HOST, SSH_KEY"
    exit 1
fi

# Determine remote path and rsync ignore file based on environment
if [ "$ENVIRONMENT" = "development" ]; then
    REMOTE_BASE="/home/ubuntu/tests"
    RSYNC_IGNORE=".rsyncignore"
    echo "Deploying to DEVELOPMENT environment"
    echo "  (All files including stats will be synced)"
elif [ "$ENVIRONMENT" = "production" ]; then
    REMOTE_BASE="/home/ubuntu/servers"
    RSYNC_IGNORE=".rsyncignore.prod"
    echo "Deploying to PRODUCTION environment"
    echo "  (User data and stats will be preserved)"
else
    echo "Error: ENVIRONMENT must be 'development' or 'production'"
    exit 1
fi

REMOTE_PATH="${REMOTE_BASE}/${SERVER_NAME}/"

echo ""
echo "Configuration:"
echo "  Server Name: $SERVER_NAME"
echo "  Party Name: $PARTY_NAME"
echo "  Port: $PORT"
echo "  Environment: $ENVIRONMENT"
echo "  Remote Path: $SSH_HOST:$REMOTE_PATH"
echo ""

# Backup original config.toml
echo "Backing up config.toml..."
cp config.toml config.toml.backup

# Update config.toml with environment variables
echo "Updating config.toml with deployment settings..."
sed -i.tmp "s/^party_name = .*/party_name = \"$PARTY_NAME\"/" config.toml
sed -i.tmp "s/^port = .*/port = $PORT/" config.toml
rm -f config.toml.tmp

echo "Modified config.toml for deployment:"
echo "  party_name = \"$PARTY_NAME\""
echo "  port = $PORT"
echo ""

# Create remote directory if it doesn't exist
echo "Ensuring remote directory exists..."
ssh -i "$SSH_KEY" "$SSH_HOST" "mkdir -p $REMOTE_PATH"

# Deploy using rsync
echo "Deploying files to server..."
echo "Using exclusion file: $RSYNC_IGNORE"
rsync -avz \
  --exclude-from="$RSYNC_IGNORE" \
  --progress \
  -e "ssh -i $SSH_KEY" \
  ./ \
  "$SSH_HOST:$REMOTE_PATH"

# Restore original config.toml
echo ""
echo "Restoring original config.toml..."
mv config.toml.backup config.toml

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================="
    echo "Deployment completed successfully!"
    echo "======================================="
    echo ""
    echo "Deployment Summary:"
    echo "  Environment: $ENVIRONMENT"
    echo "  Server Name: $SERVER_NAME"
    echo "  Party Name: $PARTY_NAME"
    echo "  Port: $PORT"
    echo "  Remote Path: $REMOTE_PATH"
    echo ""
    echo "Next steps:"
    echo "  1. SSH into server:"
    echo "     ssh -i $SSH_KEY $SSH_HOST"
    echo ""
    echo "  2. Navigate to server directory:"
    echo "     cd $REMOTE_PATH"
    echo ""
    echo "  3. Start the server:"
    echo "     ./docker.sh"
    echo ""
    echo "Quick commands:"
    echo "  ssh -i $SSH_KEY $SSH_HOST \"cd $REMOTE_PATH && ./docker.sh\""
    echo ""
else
    echo ""
    echo "Deployment failed!"
    mv config.toml.backup config.toml
    exit 1
fi
