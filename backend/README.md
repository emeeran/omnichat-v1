# OmniChat Backend

## Prerequisites
- Python 3.8+
- pip
- virtualenv

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd backend
```

2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Configure Environment
- Copy `.env.example` to `.env`
- Fill in your API keys for various providers

## Running the Application

### Development Server
```bash
flask run
```

### Production Deployment
Use a WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Supported Providers
- OpenAI
- Anthropic
- Google AI
- Deepseek
- Groq
- Mistral
- Cohere
- Gemini
- Alibaba
- OpenRouterAI
- Hugging Face

## Configuration
Edit `.env` file to set:
- API Keys
- Default Provider
- Default Model
- Logging Levels

### Environment Variables
- `DEFAULT_PROVIDER`: Set the default AI provider (default: deepseek)
- `DEFAULT_MODEL`: Set the default model for the provider (default: deepseek-chat)
- `FLASK_ENV`: Set to 'development' or 'production'

## Provider Registration
Providers can be registered dynamically through the API:
```bash
curl -X POST /api/providers/register \
     -H "Content-Type: application/json" \
     -d '{"provider_id": "openai", "api_key": "your-api-key"}'
```

## Logging
- Development mode: Detailed DEBUG logs
- Production mode: INFO level logs

## Error Handling
- Consistent error responses
- Detailed logging for troubleshooting

## Model Discovery
- Periodically refreshes supported models
- Caches model lists for performance
- Fallback to predefined models if API discovery fails

## Contributing
1. Create a virtual environment
2. Install dependencies
3. Create a `.env` file
4. Run tests
5. Submit a pull request
