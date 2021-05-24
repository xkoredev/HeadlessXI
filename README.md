# HeadlessXI

A headless client for DSP/TPZ/LSB-based servers, written in Python.

## Usage

### Requirements

Python 3.2+ (version unconfirmed, just not 2.x)

### Installation

```bash
# Using pip3, pip or whatever you have available
# Install
pip3 install git+https://github.com/zach2good/HeadlessXI.git

# Upgrade
pip3 install --upgrade git+https://github.com/zach2good/HeadlessXI.git
```

### Example

```py
from headlessxi import HXIClient

# Create a client and log in
hxi_client = HXIClient('admin', 'admin', 'localhost')
hxi_client.login()

# Wait a while for login
time.sleep(10)

# Send GM commands
hxi_client.send_say('!bring Testtwo')
time.sleep(5)

# Send /say messages
hxi_client.send_say('Hello from HXIClient!')
time.sleep(2)

# Goodbye
hxi_client.logout()
```

### Advanced Example

HeadlessXI is designed to be used for CI automation.
While features are missing (ie. most things), you can pre-populate the account and character state through the database.

#### Bash Script

```bash
printf "Installing HeadlessXI\n"
pip3 install git+https://github.com/zach2good/HeadlessXI.git

printf "\nPopulating database\n"
mysql -uroot -proot << EOF
USE xidb;

-- Clean out anything already there (just in case)
DELETE FROM accounts;
DELETE FROM chars;

-- Create an account
INSERT INTO accounts(id, login, password, timecreate, timelastmodify, status, priv)
VALUES(1000, 'admin', PASSWORD('admin'), NOW(), NOW(), 1, 1);
SELECT id, login FROM accounts;

-- Create a character
INSERT INTO chars(charid, accid, charname, pos_zone, nation, gmlevel)
VALUES(1, 1000, 'Test', 0, 0, 5);
SELECT charid, accid, pos_zone, pos_x, pos_y, pos_z FROM chars;

-- Update character information
-- Place near some Robber Crabs in Kuftal Tunnel
UPDATE chars
SET
    pos_zone = 174,
    pos_prevzone = 174,
    pos_x = 55,
    pos_y = -9,
    pos_z = -140
WHERE charid = 1;
SELECT charid, accid, pos_zone, pos_x, pos_y, pos_z FROM chars;

-- Set GodMode CharVar = 1
INSERT INTO char_vars(charid, varname, value)
VALUES(1, 'GodMode', 1);
SELECT * FROM char_vars;
EOF

printf "\nRunning HXIClient for 60 seconds\n"
python3 << EOF
from headlessxi import HXIClient
hxi_client = HXIClient('admin', 'admin', 'localhost')
hxi_client.login()
time.sleep(30)
hxi_client.logout()
EOF

printf "\n"
```

#### Output

```txt
Installing HeadlessXI
Collecting git+https://github.com/zach2good/HeadlessXI.git
  Cloning https://github.com/zach2good/HeadlessXI.git to [...]
  Running command git clone -q https://github.com/zach2good/HeadlessXI.git [...]

Populating database
id      login
1000    admin
charid  accid   pos_zone        pos_x   pos_y   pos_z
1       1000    0       0.000   0.000   0.000
charid  accid   pos_zone        pos_x   pos_y   pos_z
1       1000    174     55.000  -9.000  -140.000
charid  varname value
1       GodMode 1

Running HeadlessXI for 60 seconds
Starting up login connection on localhost port 54231
Login successful
Account ID: 1000
Starting up lobby data connection on localhost port 54230
Sending lobby_data_0xA1 (0)
Starting up lobby view connection on localhost port 54001
Sending lobby_view_0x26
Expansion bitmask: 0b111111111110 (4094)
Feature bitmask: 0b1101 (13)
Sending lobby_view_0x1F
Sending lobby_data_0xA1 (1)
Sending lobby_view_0x07
Sending lobby_data_0xA2
...
```

## Credits

- The DSP/TPZ/LSB [login server](https://github.com/LandSandBoat/server/tree/base/src/login)
- [xiloader](https://github.com/LandSandBoat/xiloader)
- bope12's C# [implementation](https://github.com/bope12/PacketFFXI), on which HeadlessXI is based
