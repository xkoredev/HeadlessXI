from .util import util, PACKET_HEAD

PD_CODE = 1

def set(data, idx, val):
    data[PACKET_HEAD + idx] = val

class packets:
    # TODO:
    @staticmethod
    def generate_starting_packet(type, size):
        global PD_CODE
        PD_CODE = PD_CODE + 1

        code_bytes = util.pack_16(PD_CODE)
        type_bytes = util.pack_16(type)
        size_bytes = util.pack_16(size)

        data = bytearray(PACKET_HEAD + size)

        # Header
        util.memcpy(code_bytes, 0, data, 0, 2)

        # Body
        util.memcpy(type_bytes, 0, data, PACKET_HEAD + 0x00, 2) # Packet Type
        util.memcpy(size_bytes, 0, data, PACKET_HEAD + 0x01, 2) # Packet Size
        util.memcpy(code_bytes, 0, data, PACKET_HEAD + 0x02, 2) # Packet Seq (not important)

        return data

    @staticmethod
    def to_map_e7():
        global PD_CODE
        PD_CODE = PD_CODE + 1

        data = bytearray(4 + PACKET_HEAD + 16)
        util.memcpy(util.pack_16(PD_CODE), 0, data, 0, 2)
        util.memcpy(util.pack_16(0xE7), 0, data, PACKET_HEAD, 2)
        data[PACKET_HEAD + 0x01] = 0x04
        util.memcpy(util.pack_16(PD_CODE), 0, data, PACKET_HEAD + 0x02, 2)
        data[PACKET_HEAD + 0x06] = 0x03

        # TODO:
        # packet = generate_starting_packet(0xE7, 4)
        # set(packet, 0x06, 0x03)
        # util.packet_md5(packet)
        # return packet

        util.packet_md5(data)
        return data

    @staticmethod
    def to_map_0d():
        global PD_CODE
        PD_CODE = PD_CODE + 1

        data = bytearray(4 + PACKET_HEAD + 16)
        util.memcpy(util.pack_16(PD_CODE), 0, data, 0, 2)
        util.memcpy(util.pack_16(0x0D), 0, data, PACKET_HEAD, 2)
        data[PACKET_HEAD + 0x01] = 0x04
        util.memcpy(util.pack_16(PD_CODE), 0, data, PACKET_HEAD + 0x02, 2)

        util.packet_md5(data)
        return data

    @staticmethod
    def to_map_b5(message):
        global PD_CODE
        PD_CODE = PD_CODE + 1

        data = bytearray(21 + 45 + PACKET_HEAD + 30)
        util.memcpy(util.pack_16(PD_CODE), 0, data, 0, 2)
        util.memcpy(util.pack_16(0x0B5), 0, data, PACKET_HEAD, 2)
        data[PACKET_HEAD + 0x01] = len(message)
        util.memcpy(util.pack_16(PD_CODE), 0, data, PACKET_HEAD + 0x02, 2)
        data[PACKET_HEAD + 0x04] = 0; # Say
        util.memcpy(util.to_bytes(message), 0, data, PACKET_HEAD + 0x06, len(message))

        util.packet_md5(data)
        return data

    @staticmethod
    def to_map_0a(char_id):
        global PD_CODE
        PD_CODE = PD_CODE + 1

        data = bytearray(136)
        util.memcpy(util.pack_16(PD_CODE), 0, data, 0, 2)
        util.memcpy(util.pack_16(0x00A), 0, data, PACKET_HEAD, 2)
        data[PACKET_HEAD + 0x01] = 0x2E
        util.memcpy(util.pack_16(PD_CODE), 0, data, PACKET_HEAD + 0x02, 2)
        util.memcpy(util.pack_32(char_id), 0, data, PACKET_HEAD + 0x0C, 4)

        util.packet_md5(data)
        return data

    @staticmethod
    def to_map_11():
        global PD_CODE
        PD_CODE = PD_CODE + 1

        data = bytearray(53)
        util.memcpy(util.pack_16(PD_CODE), 0, data, 0, 2)
        util.memcpy(util.pack_16(0x011), 0, data, PACKET_HEAD, 2)
        data[PACKET_HEAD + 0x01] = 0x04
        util.memcpy(util.pack_16(PD_CODE), 0, data, PACKET_HEAD + 0x02, 2)

        util.packet_md5(data)
        return data
