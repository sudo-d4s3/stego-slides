#!/usr/bin/env python3
import os

def read_chunks(file_path):
    with open(file_path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        signature = f.read(8)
        print(f"Signature: {signature}")

        while True:
            if f.tell() >= file_length:
                break

            length = f.read(4)
            chunk_type = f.read(4)
            chunk_content = f.read(int.from_bytes(length, byteorder='big'))
            crc = f.read(4)

            print(f"\nChunk Type: {chunk_type.decode()}")
            print(f"Size: {int.from_bytes(length, byteorder='big')}")
            print(f"CRC: {crc.hex()}")

            if chunk_type == b'IDAT':
                extract_pixels(chunk_content)

def extract_pixels(chunk_content):
    binary_message = ''.join(format(ord(c), '08b') for c in "Hack The Planet!")
    message_index = 0

    print("Pixel Data (with embedded message bits):")
    for byte in chunk_content:
        binary_byte = format(byte, '08b')
        modified_byte = binary_byte[:-1] + binary_message[message_index]
        message_index = (message_index + 1) % len(binary_message)
        modified_decimal = int(modified_byte, 2)

        print(f"{modified_decimal:02X}", end=' ')
    print()

file_path = "blank.png"
read_chunks(file_path)
