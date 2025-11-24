#!/bin/sh
# Copy the correct proxy config for Docker
cp /app/proxy.conf.docker.json /app/proxy.conf.json

# Start the Angular dev server
exec npm start -- --host 0.0.0.0 --port 4200
