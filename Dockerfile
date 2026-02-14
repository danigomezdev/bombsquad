# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (cached layer - only rebuilds if this changes)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    dbus \
    systemd \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Generate machine-id for BombSquad v2transport
RUN dbus-uuidgen > /etc/machine-id 2>/dev/null || \
    cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 > /etc/machine-id && \
    chmod 444 /etc/machine-id

# Copy only necessary binaries (cached if unchanged)
COPY bombsquad_server /app/
COPY dist/bombsquad_headless /app/dist/
RUN chmod +x bombsquad_server && \
    chmod +x dist/bombsquad_headless

# Copy Python modules required by bombsquad_server
COPY dist/ba_data /app/dist/ba_data

# Copy config and mods (these change more often)
COPY config.toml /app/
COPY dist/ba_root /app/dist/ba_root

# Copy remaining files (art, docs, etc)
COPY art.txt LICENSE README.md /app/

# Create necessary directories
RUN mkdir -p dist/ba_root/mods/stats \
    dist/ba_root/mods/playersdata \
    dist/ba_root/mods/serverdata

# Expose server port (default 6666, can be changed in config.toml)
EXPOSE 6666/udp

# Run the server
CMD ["./bombsquad_server", "--noninteractive"]
