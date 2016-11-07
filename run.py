import os
# Run a test server.
port = int(os.getenv('VCAP_APP_PORT', '5050'))

from app import app
app.run(host='0.0.0.0', port=int(port), debug=True)
