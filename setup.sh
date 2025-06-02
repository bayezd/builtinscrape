#!/bin/bash
# Install required dependencies for the analyzer

echo "Installing required Python packages..."
pip install requests python-dotenv

echo "Creating .env file if it doesn't exist..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it to add your OpenRouter API key."
else
    echo ".env file already exists."
fi

echo "Setup complete!"
echo "To run the analyzer, use: python analyze.py --api-key YOUR_OPENROUTER_API_KEY"
echo "Or add your API key to the .env file and run: python analyze.py"
