# HeadlessXI
A headless client for DSP/TPZ/LSB-based servers, written in Python.

## Usage
```py
from headlessxi import HeadlessXIClient

# Create a client and log in
hxi_client = HeadlessXIClient("admin", "admin", "localhost")
hxi_client.login()

# Wait a while for login
time.sleep(10)

# Send GM commands
hxi_client.send_say("!bring Testtwo")
time.sleep(5)

# Send /say messages
hxi_client.send_say("Hello from HeadlessXIClient!")
time.sleep(2)

# Goodbye
hxi_client.logout()
```

## Credits
- The DSP/TPZ/LSB [login server](https://github.com/LandSandBoat/server/tree/base/src/login)
- [xiloader](https://github.com/LandSandBoat/xiloader)
- bope12's C# [implementation](https://github.com/bope12/PacketFFXI), on which HeadlessXI is based
