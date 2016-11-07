import os
# Run a test server.
porta = int(os.getenv('PORT'))

from app import app
app.run(host='0.0.0.0', port=porta, debug=True)
