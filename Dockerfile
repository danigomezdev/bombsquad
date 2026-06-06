FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN dbus-uuidgen > /etc/machine-id 2>/dev/null || \
    cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 > /etc/machine-id && \
    chmod 444 /etc/machine-id

# Copy server binaries and scripts
COPY bombsquad_server /app/
COPY dist/ballisticakit_server /app/
COPY dist/dist/ballisticakit_headless /app/dist/
RUN chmod +x bombsquad_server dist/ballisticakit_headless && \
    ln -s ballisticakit_headless dist/bombsquad_headless

# Copy Python modules
COPY dist/dist/ba_data /app/dist/ba_data

# Copy config
COPY config.toml /app/

# Create data directories
RUN mkdir -p dist/ba_root/mods

EXPOSE 43210/udp

CMD ["./ballisticakit_server", "--noninteractive"]
