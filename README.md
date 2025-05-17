# OmniChat v1

OmniChat is a versatile chat application designed to integrate seamlessly with multiple AI providers, offering users a flexible and powerful conversational experience. This project aims to provide a unified interface for interacting with various AI models, with support for dynamic model selection and provider management.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Provider Integration](#provider-integration)
- [Model Updates](#model-updates)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview
OmniChat allows users to interact with AI models from different providers such as OpenAI, Groq, Anthropic, and more. The application supports automatic provider registration based on API keys, dynamic model fetching, and a user-friendly interface for selecting providers and models.

## Features
- **Multi-Provider Support**: Connect with various AI providers using their API keys.
- **Dynamic Model Selection**: Choose from a list of models fetched directly from provider APIs.
- **Auto-Registration**: Providers are automatically registered when API keys are added to the environment.
- **Periodic Model Updates**: Weekly updates to ensure the latest models are available.
- **User Interface**: Intuitive frontend for managing chats, providers, and settings.
- **Performance Optimization**: Caching and code compaction for faster interactions.

## Installation
### Prerequisites
- Python 3.8+ for backend
- Node.js and npm for frontend
- API keys for desired AI providers

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/omnichat-v1.git
   cd omnichat-v1
   ```
2. Set up the backend environment:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env to add your API keys
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python run.py
   ```

### Frontend Setup
1. Set up the frontend environment:
   ```bash
   cd frontend
   npm install
   ```
2. Run the frontend development server:
   ```bash
   npm run dev
   ```

## Usage
- Access the application via the frontend URL (typically `http://localhost:5173`).
- Select a provider and model from the interface.
- Start chatting with the AI model of your choice.

## Project Structure
```
omnichat-v1/
├── backend/                    # Backend server and API logic
│   ├── app/                    # Core application code
│   │   ├── services/           # AI provider integrations and services
│   │   │   └── ai_providers/   # Individual provider implementations
│   │   ├── routes/             # API endpoints
│   │   └── models/             # Database models (if applicable)
│   ├── scripts/                # Maintenance scripts
│   │   └── update_models.py    # Script for updating model lists
│   ├── tests/                  # Unit tests for backend components
│   └── prd.md                  # Product Requirements Document
├── frontend/                   # Frontend React application
│   ├── src/                    # Source code for frontend
│   │   ├── components/         # React components for UI
│   │   └── services/           # API interaction services
│   └── public/                 # Static assets
├── to_delete/                  # Directory for redundant or obsolete files
└── README.md                   # Project documentation
```

## Provider Integration
OmniChat supports multiple AI providers. To add a new provider:
1. Add the API key to the `./backend/.env` file.
2. The provider will be auto-registered by the application.
3. If a provider file does not exist, it will be dynamically created with supported models and necessary configurations.

## Model Updates
To ensure the latest models are available:
- Run the model update script weekly:
  ```bash
  python backend/scripts/update_models.py
  ```
- This script clears cached model lists and fetches the latest models from each provider's API.

## Testing
Run unit tests to verify functionality:
```bash
cd backend
python -m unittest discover tests
```

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
