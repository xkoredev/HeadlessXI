import hashlib
import struct

# Globals
PACKET_HEAD = 28

class util:
    @staticmethod
    def to_bytes(val):
        return bytes(val, encoding="utf-8")

    @staticmethod
    def memcpy(src, src_offset, dst, dst_offset, count):
        try:
            src_bytes = util.to_bytes(src[src_offset:])
        except:
            src_bytes = src

        try:
            dst_bytes = util.to_bytes(dst[dst_offset:])
        except:
            dst_bytes = dst

        for idx in range(count):
            dst_bytes[dst_offset + idx] = src_bytes[src_offset + idx]

    @staticmethod
    def unpack_uint16(data, offset):
        return struct.unpack_from('<H', data, offset)[0]

    @staticmethod
    def unpack_uint32(data, offset):
        return struct.unpack_from('<I', data, offset)[0]

    @staticmethod
    def pack_16(data):
        return struct.pack('<H', data)

    @staticmethod
    def pack_32(data):
        return struct.pack('<I', data)

    def int_to_ip(ip):
        return '.'.join([str((ip >> 8 * i) % 256) for i in [3, 2, 1, 0]])

    @staticmethod
    def packet_addmd5(data):
        to_md5 = bytearray(len(data) - (PACKET_HEAD + 16))
        util.memcpy(data, PACKET_HEAD, to_md5, 0, len(to_md5))
        to_md5 = hashlib.md5(to_md5)
        util.memcpy(to_md5.digest(), 0, data, len(data) - 16, 16)
