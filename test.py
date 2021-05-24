import time
from headlessxi import HXIClient

# Create a client and log in
hxi_client = HXIClient('admin', 'admin', 'localhost')
hxi_client.login()

# Wait a while for login
time.sleep(10)

# Send /say messages
hxi_client.send_say('Hello')
time.sleep(2)

# Goodbye
hxi_client.logout()
