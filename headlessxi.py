import socket
import re
import time
import threading
import errno
import hashlib
import blowfish
from util import util, PACKET_HEAD

class HeadlessXIClient:
    def __init__(self, username, password, server, slot = 1):
        self.username = username
        self.password = password
        self.server = server
        self.slot = slot

        self.char_id = 1

        self.PD_CODE = 1

    def login(self):
        self.login_connect()

        data = bytearray(33)
        util.memcpy(self.username, 0, data, 0, len(self.username))
        util.memcpy(self.password, 0, data, 16, len(self.password))
        data[32] = 0x10 # Login

        self.login_sock.sendall(data)

        in_data = self.login_sock.recv(16)
        self.login_sock.close()

        if in_data[0] == 0x01:
            print("Login successful")
            self.account_id = util.unpack_uint16(in_data, 1)
            print("Account ID: " + str(self.account_id))

            # Connect
            self.lobby_data_connect()
            self.lobby_data_0xA1_0()
            self.lobby_view_connect()
            self.lobby_view_0x26()
            self.lobby_view_0x1F()
            self.lobby_data_0xA1_1()
            self.lobby_view_0x24()
            self.lobby_view_0x07()
            self.lobby_data_0xA2()
            self.start_map_listener()

            # Map
            self.map_login_to_zone()
        else:
            print("Error logging in, aborting!...")
            exit(-1)

    def logout(self):
        self.map_send_logout()
        self.stop_map_listener()

    def login_connect(self):
        server_address = (self.server, 54231)
        print('Starting up login connection on %s port %s' % server_address)
        self.login_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login_sock.connect(server_address)

    def lobby_data_connect(self):
        server_address = (self.server, 54230)
        print('Starting up lobby data connection on %s port %s' % server_address)
        self.lobbydata_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lobbydata_sock.connect(server_address)

    def lobby_view_connect(self):
        server_address = (self.server, 54001)
        print('Starting up lobby view connection on %s port %s' % server_address)
        self.lobbyview_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lobbyview_sock.connect(server_address)

    def lobby_data_0xA1_0(self):
        print("Sending lobby_data_0xA1 (0)")
        try:
            data = bytearray(5)
            data[0] = 0xA1
            util.memcpy(util.pack_32(self.account_id), 0, data, 1, 4)
            self.lobbydata_sock.sendall(data)
        except Exception as ex:
            print(ex)

    def lobby_view_0x26(self):
        print("Sending lobby_view_0x26")
        try:
            data = bytearray(152)
            data[8] = 0x26
            version = "30210400_0"
            util.memcpy(version, 0, data, 116, 10)
            self.lobbyview_sock.sendall(data)

            in_data = self.lobbyview_sock.recv(40)

            expansion_bitmask = util.unpack_uint32(in_data, 32)
            print("Expansion bitmask: " + str(bin(expansion_bitmask)) + " (" + str(expansion_bitmask) + ")")

            feature_bitmask = util.unpack_uint16(in_data, 36)
            print("Feature bitmask: " + str(bin(feature_bitmask)) + " (" + str(feature_bitmask) + ")")
        except Exception as ex:
            print(ex)

    def lobby_view_0x1F(self):
        print("Sending lobby_view_0x1F")
        try:
            data = bytearray(44)
            data[8] = 0x1F
            self.lobbyview_sock.sendall(data)
        except Exception as ex:
            print(ex)

    def lobby_data_0xA1_1(self):
        print("Sending lobby_data_0xA1 (1)")
        try:
            # Should send 9 bytes: A1 00 00 01 00 00 00 00 00
            data = bytearray.fromhex('A10000010000000000')

            # Sends: bytearray(b'\xa1\x00\x00\x01\x00\x00\x00\x00\x00')
            self.lobbydata_sock.sendall(data)

            _ = self.lobbydata_sock.recv(328)
            data = self.lobbyview_sock.recv(2272)

            if data[36] != 0 and data[36 + self.slot * 140] != 0:
                self.char_id = util.unpack_uint32(data, 36 + (self.slot * 140))
                
                # TODO: This isn't good
                self.char_name = data[44 + (self.slot * 140):44 + (self.slot * 140) + 16].decode('utf-8', 'ignore')
                self.char_name = re.sub(r'\d+', '', self.char_name)

                print(self.char_id, self.char_name)
        except Exception as ex:
            print(ex)

    def lobby_view_0x24(self):
        # print("Sending lobby_view_0x24")
        pass

    def lobby_view_0x07(self):
        print("Sending lobby_view_0x07")
        try:
            data = bytearray(88)
            data[8] = 0x07
            util.memcpy(util.pack_32(self.char_id), 0, data, 28, 4)
            self.lobbyview_sock.sendall(data)
        except Exception as ex:
            print(ex)

    def lobby_data_0xA2(self):
        print("Sending lobby_data_0xA2")
        time.sleep(0.5)
        data = bytearray([0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x58, 0xE0, 0x5D, 0xAD, 0x00, 0x00, 0x00, 0x00])
        self.lobbydata_sock.sendall(data)

        data = self.lobbyview_sock.recv(0x48)

        try:
            self.zone_ip = util.int_to_ip(socket.htonl(util.unpack_uint32(data, 0x38)))
            self.zone_port = util.unpack_uint16(data, 0x3C)
            self.search_ip = util.int_to_ip(socket.htonl(util.unpack_uint32(data, 0x40)))
            self.search_port = util.unpack_uint16(data, 0x44)
        except Exception as ex:
            print("Could not get information for map server handoff!")
            print(ex)
            exit(-1)

        print(f"ZoneIP/Port: {self.zone_ip}:{self.zone_port}, SearchIP:Port: {self.search_ip}/{self.search_port}")

    def start_map_listener(self):
        print("Starting listener to map server")
        self.map_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.map_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.map_sock.setblocking(False)
        self.map_sock.connect((self.zone_ip, self.zone_port))

        self.map_thread = threading.Thread(target=self.map_sock_listen, args=())
        self.map_thread.daemon = True
        self.map_thread_listening = True
        self.map_thread.start()

    def map_sock_listen(self):
        while self.map_thread_listening == True:
            try:
                data = self.map_sock.recv(4096)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    time.sleep(1)
                    continue
                else:
                    print(e)
                    exit(-1)
            else:
                self.parse_incoming_packet(data)

    def parse_incoming_packet(self, data):
        #print(f"recv: {data.hex()}")
        server_packet_id = util.unpack_uint16(data, 0)
        client_packet_id = util.unpack_uint16(data, 2)
        packet_time = util.unpack_uint32(data, 8)

    def stop_map_listener(self):
        print("Closing listener to map server")
        self.map_thread_listening = False
        self.map_thread.join()

    def map_login_to_zone(self):
        starting_key = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0xAD5DE056]
        starting_key[4] = starting_key[4] + 2
        byte_array = bytearray(len(starting_key) * 4)

        util.memcpy(util.pack_32(starting_key[0]), 0, byte_array, 0, 4)
        util.memcpy(util.pack_32(starting_key[1]), 0, byte_array, 4, 4)
        util.memcpy(util.pack_32(starting_key[2]), 0, byte_array, 8, 4)
        util.memcpy(util.pack_32(starting_key[3]), 0, byte_array, 12, 4)
        util.memcpy(util.pack_32(starting_key[4]), 0, byte_array, 16, 4)

        print("Blowfish Key: " + byte_array.hex().strip('0'))

        hash_key = hashlib.md5(byte_array).digest()

        for i in range(16):
            if hash_key[i] == 0:
                zero = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                util.memcpy(zero, i, hash_key, i, 16 - i)

        self.bf = blowfish.Blowfish(hash_key)

        # 0x0A
        data = bytearray(136)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, 0, 2) # Packet Count
        util.memcpy(util.pack_16(0x0A), 0, data, PACKET_HEAD, 2) # Packet Type
        data[PACKET_HEAD + 1] = 0x2E # Size
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, PACKET_HEAD + 0x02, 2) # Packet Count
        util.memcpy(util.pack_32(self.char_id), 0, data, PACKET_HEAD + 0x0C, 4)
        util.packet_addmd5(data)
        self.map_sock.sendto(data, (self.zone_ip, self.zone_port))

        # 0x11
        self.PD_CODE = self.PD_CODE + 1
        data = bytearray(53)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, 0, 2) # Packet Count
        util.memcpy(util.pack_16(0x11), 0, data, PACKET_HEAD, 2) # Packet Type
        data[PACKET_HEAD + 1] = 0x04 # Size
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, PACKET_HEAD + 0x02, 2) # Packet Count
        util.packet_addmd5(data)
        self.map_sock.sendto(data, (self.zone_ip, self.zone_port))

    def send_say(self, message):
        print(f"Sending /say: {message}")
        self.PD_CODE = self.PD_CODE + 1
        data = bytearray(21 + 45 + PACKET_HEAD + 30)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, 0, 2) # Packet Count
        util.memcpy(util.pack_16(0x0B5), 0, data, PACKET_HEAD, 2) # Packet Type
        data[PACKET_HEAD + 0x01] = len(message)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, PACKET_HEAD + 0x02, 2) # Packet Count
        data[PACKET_HEAD + 0x04] = 0; # Say
        util.memcpy(util.to_bytes(message), 0, data, PACKET_HEAD + 0x06, len(message))
        util.packet_addmd5(data)
        self.map_sock.sendto(data, (self.zone_ip, self.zone_port))

    def map_send_logout(self):
        print("Sending map_send_logout")

        self.PD_CODE = self.PD_CODE + 1
        data = bytearray(4 + PACKET_HEAD + 16)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, 0, 2) # Packet Count
        util.memcpy(util.pack_16(0xE7), 0, data, PACKET_HEAD, 2) # Packet Type
        data[PACKET_HEAD + 0x01] = 0x04
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, PACKET_HEAD + 0x02, 2) # Packet Count
        data[PACKET_HEAD + 0x06] = 0x03; # Say
        util.packet_addmd5(data)
        self.map_sock.sendto(data, (self.zone_ip, self.zone_port))

        self.PD_CODE = self.PD_CODE + 1
        data = bytearray(4 + PACKET_HEAD + 16)
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, 0, 2) # Packet Count
        util.memcpy(util.pack_16(0x0D), 0, data, PACKET_HEAD, 2) # Packet Type
        data[PACKET_HEAD + 0x01] = 0x04
        util.memcpy(util.pack_16(self.PD_CODE), 0, data, PACKET_HEAD + 0x02, 2) # Packet Count
        util.packet_addmd5(data)
        self.map_sock.sendto(data, (self.zone_ip, self.zone_port))
