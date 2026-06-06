#!/bin/bash
set -e

# BombSquad Server Docker Manager
# Manages Docker container lifecycle with unique names per server

echo "======================================="
echo "BombSquad Server Docker Manager"
echo "======================================="
echo ""

# Auto-detect project name from directory (e.g., less_east_c1)
CURRENT_DIR=$(basename "$PWD")
export COMPOSE_PROJECT_NAME="${CURRENT_DIR}"

# Try to read PORT from config.toml
if [ -f "config.toml" ]; then
    PORT_FROM_CONFIG=$(grep "^port = " config.toml | sed 's/port = //' | tr -d ' ')
    if [ ! -z "$PORT_FROM_CONFIG" ]; then
        export PORT="$PORT_FROM_CONFIG"
    fi
fi

# Set default port if not found
export PORT="${PORT:-6666}"

CONTAINER_NAME="${COMPOSE_PROJECT_NAME}-server"
IMAGE_NAME="bombsquad-server:${COMPOSE_PROJECT_NAME}"

echo "Server Configuration:"
echo "  Project Name: $COMPOSE_PROJECT_NAME"
echo "  Container: $CONTAINER_NAME"
echo "  Port: $PORT"
echo ""

# Docker compose command
DOCKER_COMPOSE="docker compose"

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker compose is available
if ! $DOCKER_COMPOSE version &> /dev/null 2>&1; then
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    else
        echo "Error: Docker Compose is not installed."
        exit 1
    fi
fi

# Check Docker permissions
if ! docker ps &> /dev/null 2>&1; then
    echo "Error: Cannot connect to Docker daemon."
    echo "Make sure Docker is running and you have permissions."
    echo ""
    echo "Try: sudo usermod -aG docker $USER"
    echo "Then log out and log back in."
    exit 1
fi

# Function to check if image exists
image_exists() {
    docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${IMAGE_NAME}$"
}

# Function to check if container is running
container_running() {
    docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"
}

# Function to check if container exists (stopped or running)
container_exists() {
    docker ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"
}

# Menu
echo "Select an option:"
echo "1) Start server (build if needed)"
echo "2) Stop server"
echo "3) Restart server (config/mods changes only)"
echo "4) Rebuild and restart (code changes)"
echo "5) View logs (live)"
echo "6) View logs (last 200 lines)"
echo "7) Force full rebuild (clean rebuild)"
echo "8) Server status"
echo "9) Enter container shell"
echo "0) Stop and remove container"
echo ""
read -p "Enter option [0-9]: " option

case $option in
    1)
        echo "Starting BombSquad server..."
        echo ""

        if container_running; then
            echo "Server is already running!"
            echo ""
            echo "Recent logs:"
            $DOCKER_COMPOSE logs --tail=20
        elif container_exists; then
            echo "Container exists but is stopped. Removing old container..."
            docker rm "$CONTAINER_NAME"
            echo "Creating and starting new container..."
            if image_exists; then
                $DOCKER_COMPOSE up -d
            else
                echo "Building image for the first time..."
                $DOCKER_COMPOSE up -d --build
            fi
            echo ""
            echo "Server started!"
            echo ""
            echo "Recent logs:"
            $DOCKER_COMPOSE logs --tail=20
        else
            if image_exists; then
                echo "Image found. Starting server without rebuild..."
                $DOCKER_COMPOSE up -d
            else
                echo "Image not found. Building for the first time..."
                $DOCKER_COMPOSE up -d --build
            fi
            echo ""
            echo "Server started!"
            echo ""
            echo "Recent logs:"
            $DOCKER_COMPOSE logs --tail=20
        fi
        ;;

    2)
        echo "Stopping BombSquad server..."
        if container_running; then
            $DOCKER_COMPOSE stop
            echo "Server stopped."
        else
            echo "Server is not running."
        fi
        ;;

    3)
        echo "Restarting BombSquad server..."
        echo "This only reloads mounted files (config.toml, mods)"
        echo ""
        if container_exists; then
            $DOCKER_COMPOSE restart
            echo ""
            echo "Server restarted!"
            echo ""
            echo "Recent logs:"
            $DOCKER_COMPOSE logs --tail=20
        else
            echo "Container doesn't exist. Use option 1 to start."
        fi
        ;;

    4)
        echo "Quick rebuild (with cache)..."
        echo "Use this after deploying code changes"
        echo ""
        echo "Stopping container..."
        $DOCKER_COMPOSE down
        echo ""
        echo "Rebuilding image (using cache for faster build)..."
        $DOCKER_COMPOSE build
        echo ""
        echo "Starting server with updated image..."
        $DOCKER_COMPOSE up -d
        echo ""
        echo "Rebuild complete!"
        echo ""
        echo "Recent logs:"
        $DOCKER_COMPOSE logs --tail=30
        ;;

    5)
        echo "Showing live logs (Ctrl+C to exit)..."
        $DOCKER_COMPOSE logs -f --tail=100
        ;;

    6)
        echo "Showing logs (last 200 lines)..."
        $DOCKER_COMPOSE logs --tail=200
        ;;

    7)
        echo "Force full rebuild (clean rebuild, no cache)..."
        echo ""
        read -p "This will rebuild the entire image from scratch. Continue? (yes/no): " confirm
        if [ "$confirm" = "yes" ] || [ "$confirm" = "y" ]; then
            echo "Stopping container if running..."
            $DOCKER_COMPOSE down
            echo ""
            echo "Rebuilding image from scratch (no cache)..."
            $DOCKER_COMPOSE build --no-cache
            echo ""
            echo "Starting server with new image..."
            $DOCKER_COMPOSE up -d
            echo ""
            echo "Rebuild complete!"
            echo ""
            echo "Recent logs:"
            $DOCKER_COMPOSE logs --tail=20
        else
            echo "Rebuild cancelled."
        fi
        ;;

    8)
        echo "Server status:"
        echo ""
        echo "Project: $COMPOSE_PROJECT_NAME"
        echo "Container: $CONTAINER_NAME"
        echo "Port: $PORT"
        echo ""
        $DOCKER_COMPOSE ps
        echo ""

        if image_exists; then
            echo "Image: exists ($IMAGE_NAME)"
        else
            echo "Image: not built"
        fi

        if container_running; then
            echo "Container: running"
        elif container_exists; then
            echo "Container: stopped"
        else
            echo "Container: not created"
        fi
        echo ""
        echo "All BombSquad containers on this machine:"
        docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAME|server" || echo "No containers found"
        ;;

    9)
        echo "Entering container shell..."
        if container_running; then
            echo "Type 'exit' to leave the container."
            echo ""
            docker exec -it "$CONTAINER_NAME" bash
        else
            echo "Error: Container is not running."
            echo "Start the server first (option 1)."
        fi
        ;;

    0)
        echo "Stopping and removing container..."
        echo ""
        read -p "Keep volumes (player data, stats)? (yes/no): " keep_volumes

        if [ "$keep_volumes" = "yes" ] || [ "$keep_volumes" = "y" ]; then
            $DOCKER_COMPOSE down
            echo "Container removed. Volumes preserved."
        else
            $DOCKER_COMPOSE down -v
            echo "Container and volumes removed."
        fi
        ;;

    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo ""
echo "Done!"
