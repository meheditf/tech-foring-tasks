#!/bin/bash

# Define paths for clarity
WORKSPACE_DIR="/var/lib/jenkins/workspace/tech-foring"
DEPLOY_DIR="/var/www/html/tech-foring"
ENV_FILE=".env"
ENV_FILE_PATH="/var/lib/jenkins/workspace/secrets/tasks/$ENV_FILE"

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
sudo cp "$ENV_FILE_PATH" "$DEPLOY_DIR/"

# Now, continue with the directory copying
echo "Copying the project directory..."
sudo cp -rf "$WORKSPACE_DIR/" "$DEPLOY_DIR/"

# Check if the copy operation was successful
if [ $? -eq 0 ]; then
  echo "Project directory copied successfully."
  echo "Removing the directory from the Jenkins Workspace."
  sudo rm -rf "$DEPLOY_DIR"
  echo "Removed successfully!"
else
  echo "Failed to copy the project directory."
  exit 1
fi

echo "Deployment completed successfully."
