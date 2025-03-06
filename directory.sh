#!/bin/bash

# Define paths for clarity
WORKSPACE_DIR="/var/lib/jenkins/workspace/Django-CI-CD"
DEPLOY_DIR="/var/www/html/tech-foring"
ENV_FILE=".env"
ENV_FILE_PATH="/var/lib/jenkins/workspace/secrets/tasks/$ENV_FILE"

echo "Source Directory: $WORKSPACE_DIR"
echo "Destination Directory: $DEPLOY_DIR"

# Check if source directory exists
if [ ! -d "$WORKSPACE_DIR" ]; then
  echo "Source directory does not exist: $WORKSPACE_DIR"
  exit 1
fi

# Create destination directory if it does not exist
if [ ! -d "$DEPLOY_DIR" ]; then
  echo "Destination directory does not exist. Creating it..."
  sudo mkdir -p "$DEPLOY_DIR" || { echo "Failed to create destination directory"; exit 1; }
  echo "Destination directory created: $DEPLOY_DIR"
else
  echo "Destination directory already exists: $DEPLOY_DIR"
fi

# Set correct permissions for the destination directory
echo "Setting permissions for destination directory..."
sudo chown -R jenkins:www-data "$DEPLOY_DIR" || { echo "Failed to set ownership"; exit 1; }
sudo chmod -R 775 "$DEPLOY_DIR" || { echo "Failed to set permissions"; exit 1; }

echo "Replacing secrets & .env"

# Remove existing .env file if it exists in the destination
if [ -f "$DEPLOY_DIR/$ENV_FILE" ]; then
  echo "Removing old .env file in destination..."
  sudo rm "$DEPLOY_DIR/$ENV_FILE"
else
  echo "No old .env file found in destination."
fi

# Copy the .env file from the workspace to the deploy directory
echo "Copying .env file from workspace to deployment directory..."
sudo cp "$ENV_FILE_PATH" "$DEPLOY_DIR/" || { echo "Failed to copy .env file"; exit 1; }

# Now, continue with the directory copying
echo "Copying the project directory..."
sudo cp -rf "$WORKSPACE_DIR/"* "$DEPLOY_DIR/" || { echo "Failed to copy project directory"; exit 1; }

# Check if the copy operation was successful
if [ $? -eq 0 ]; then
  echo "Project directory copied successfully."
else
  echo "Failed to copy the project directory."
  exit 1
fi
