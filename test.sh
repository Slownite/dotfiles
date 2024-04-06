#!/usr/bin/env sh

# Stop the container if it's running
docker stop setup-dotfiles-container 2>/dev/null || true

# Remove the existing container if it exists
docker rm setup-dotfiles-container 2>/dev/null || true

# Optionally, remove the existing image if it exists
# Be cautious with this step; you might want to keep the base image around
# to avoid redownloading or rebuilding it entirely.
docker rmi setup-dotfiles 2>/dev/null || true

# Build the Docker image
docker build -t setup-dotfiles -f testing_dockerfile_environment .

# Run the container
docker run --name setup-dotfiles-container setup-dotfiles
#docker run -it --name setup-dotfiles-container --entrypoint sh setup-dotfiles #debug purposes

# Uncomment the following line if you want to automatically connect to the container's shell after it starts
#docker exec -it setup-dotfiles-container sh
