# HeadlessXI
A headless client for DSP/TPZ/LSB-based servers, written in Python.

## Usage
```py
from client import Client

# Create a client and log in
client = Client("admin", "admin", "localhost")
client.login()

# Wait a while for login
time.sleep(10)

# Send GM commands
client.send_tell("!bring Testtwo")

# Goodbye
client.logout()
```

## Credits
- The DSP/TPZ/LSB [login server](https://github.com/LandSandBoat/server/tree/base/src/login)
- [xiloader](https://github.com/LandSandBoat/xiloader)
- bope12's C# [implementation](https://github.com/bope12/PacketFFXI), on which HeadlessXI is based
