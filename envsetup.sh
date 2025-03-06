#!/bin/bash

# Navigate to the deployment directory
cd /var/www/html/tech-foring || { echo "Failed to navigate to /var/www/html/tech-foring"; exit 1; }

# Check if the virtual environment already exists
if [ -d "venv" ]; then
  echo "Python virtual environment exists."
else
  echo "Creating Python virtual environment..."
  python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }
fi

# Activate the virtual environment
echo "Present Directory: $PWD"
activate () {
    . /var/www/html/tech-foring/venv/bin/activate
}
activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

echo "Virtual environment setup completed successfully."