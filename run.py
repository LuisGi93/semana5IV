import os
# Run a test server.
port = os.getenv('VCAP_APP_PORT', '5000')

from app import app
app.run(host='0.0.0.0', port=int(port))
