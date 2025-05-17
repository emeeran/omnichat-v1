from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import os
# Environment variable debugging disabled

from app import create_app

app = create_app()

if __name__ == "__main__":
    import sys
    port = int(os.getenv('PORT', 5000))
    for arg in sys.argv[1:]:
        if arg.startswith('--port='):
            try:
                port = int(arg.split('=')[1])
            except ValueError:
                print(f"Invalid port value: {arg.split('=')[1]}, using default port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
