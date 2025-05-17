#!/bin/bash

# Ensure script is run from the backend directory
cd "$(dirname "$0")"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python 3
if ! command_exists python3; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_PYTHON_VERSION="3.8"

# Compare Python versions
if [ "$(printf '%s\n' "$REQUIRED_PYTHON_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_PYTHON_VERSION" ]; then
    echo "Error: Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt

# Set up environment variables
if [ ! -f .env ]; then
    cat > .env << EOL
# Default configuration for OmniChat Backend
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(16))")

# Default Provider Configuration
DEFAULT_PROVIDER=deepseek
DEFAULT_MODEL=deepseek-chat

# Provider API Keys (replace with your actual keys)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
DEEPSEEK_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
COHERE_API_KEY=
GEMINI_API_KEY=
ALIBABA_API_KEY=
OPENROUTERAI_API_KEY=
HUGGINGFACE_API_KEY=
EOL
    echo "Created .env file with default configuration"
fi

# Optional: Run database migrations if applicable
# Uncomment and modify as needed
# flask db upgrade

# Print completion message
echo "Backend setup complete."
echo "Activate the virtual environment with: source venv/bin/activate"
echo "Run the application with: flask run"

# Optionally start the server
read -p "Do you want to start the development server? (y/n) " start_server
if [[ $start_server == "y" ]]; then
    flask run
fi
