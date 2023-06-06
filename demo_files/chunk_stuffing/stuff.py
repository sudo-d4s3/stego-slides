#!/usr/bin/env python3
import os
import binascii

def read_chunks(file_path):
    with open(file_path, 'rb') as f, open(out_file, 'wb') as of:
        f.seek(0,os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        signature = f.read(8)


        while True:
            if f.tell() >= file_length:
                print("Unable to find IEND")
                break

            length = f.read(4)
            chunk_type = f.read(4)
            chunk_content = f.read(int(length.hex(),16))
            crc = f.read(4)

            if chunk_type == b"IEND":
                rewind_bytes = 12 + int(length.hex(),16) 
                f.seek(f.tell() - rewind_bytes)
                byte_index = f.tell()
                f.seek(0)

                of.write(f.read(byte_index))
                of.write(create_chunk(b'stEg'))

                f.seek(byte_index)
                iend_len = f.read(4)
                iend_type = f.read(4)
                iend_content = f.read(int(iend_len.hex(),16))
                iend_crc = f.read(4)

                of.write(iend_len)
                of.write(iend_type)
                of.write(iend_content)
                of.write(iend_crc)
                break

def inject_file_hex(file_injection):
    with open(file_injection, 'rb') as f:
        f.seek(0,os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        file_hex = f.read()
        return file_length, file_hex

def create_chunk(chunk_name):
    max_chunk_size = 2147483647
    flength, fhex = inject_file_hex(file_injection)
    if flength > max_chunk_size:
        print("Injection file too big")
        quit()
    tmp_bytes = bytearray()
    tmp_bytes.extend(chunk_name)
    tmp_bytes.extend(fhex)
    chunk_inject = bytearray()

    chunk_inject.extend(flength.to_bytes(4,'big'))
    chunk_inject.extend(tmp_bytes)

    crc = binascii.crc32(tmp_bytes)
    crc_bytes = crc.to_bytes(4,"big")
    chunk_inject.extend(crc_bytes)
    #with open(debug_out,'wb') as debug_file:
        #debug_file.write(chunk_inject)
    #print(chunk_inject)
    return chunk_inject
    

file_path = "rgb_uncompressed.png"
file_injection = "inject"
#debug_out = "debug.png"
out_file = "out.png"
read_chunks(file_path)
