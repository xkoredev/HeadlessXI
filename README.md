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
SELECT charid, accid, charname, pos_zone, nation, gmlevel FROM chars;

-- Set char_look (default is 0 and trips up scripting)
INSERT INTO char_look (charid, face, race, size, head, body, hands, legs, feet, main, sub, ranged)
VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);
SELECT charid, face, race FROM char_look;

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
print('Sleeping 30s')
time.sleep(30)
hxi_client.logout()
EOF
```

#### Output

```txt
Installing HeadlessXI
Collecting git+https://github.com/zach2good/HeadlessXI.git
  Cloning https://github.com/zach2good/HeadlessXI.git to /tmp/pip-req-build-f6opnkjm
  Running command git clone -q https://github.com/zach2good/HeadlessXI.git /tmp/pip-req-build-f6opnkjm
Building wheels for collected packages: headlessxi
  Building wheel for headlessxi (setup.py): started
  Building wheel for headlessxi (setup.py): finished with status 'done'
  Created wheel for headlessxi: filename=headlessxi-0.1-py3-none-any.whl size=32879 sha256=43ac6579c9a97604cf891ac66dc7c10c6a3635c7722d1b03d77a048523939289
  Stored in directory: /tmp/pip-ephem-wheel-cache-vr2t592_/wheels/ff/30/84/b419d6667464aa1d28a44679cd328417d171d314033a32fbed
Successfully built headlessxi
Installing collected packages: headlessxi
Successfully installed headlessxi-0.1

Populating database
id	login
1000	admin
charid  accid   charname        pos_zone        nation  gmlevel
1       1000    Test    0       0       5
charid	face	race
1	1	1
charid	accid	pos_zone	pos_x	pos_y	pos_z
1	1000	174	55.000	-9.000	-140.000
charid	varname	value
1	GodMode	1

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
ZoneServ: ('127.0.0.1', 54230), SearchServ: ('161.0.0.1', 54002)
Starting listener to map server
Sleeping 30s
Sending map_send_logout
Closing listener to map server
```

## Credits

- The DSP/TPZ/LSB [login server](https://github.com/LandSandBoat/server/tree/base/src/login)
- [xiloader](https://github.com/LandSandBoat/xiloader)
- bope12's C# [implementation](https://github.com/bope12/PacketFFXI), on which HeadlessXI is based
