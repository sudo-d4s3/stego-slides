#!/usr/bin/env python3
import os

def read_chunks(file_path):
    with open(file_path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        signature = f.read(8)

        chunks = []

        while True:
            if f.tell() >= file_length:
                break

            length = f.read(4)
            chunk_type = f.read(4)
            chunk_content = f.read(int.from_bytes(length, byteorder='big'))
            crc = f.read(4)

            chunks.append((length, chunk_type, chunk_content, crc))

        # Write modified pixel data to a new file
        modified_chunks = modify_pixel_data(chunks)
        write_png_file(signature, modified_chunks)

def modify_pixel_data(chunks):
    binary_message = ''.join(format(ord(c), '08b') for c in "Hack The Planet!")
    message_index = 0

    modified_chunks = []

    for length, chunk_type, chunk_content, crc in chunks:
        if chunk_type == b'IDAT':
            modified_content = bytearray()

            for byte in chunk_content:
                binary_byte = format(byte, '08b')
                modified_byte = binary_byte[:-1] + binary_message[message_index]
                message_index = (message_index + 1) % len(binary_message)
                modified_decimal = int(modified_byte, 2)
                modified_content.append(modified_decimal)

            modified_chunks.append((length, chunk_type, modified_content, crc))
        else:
            modified_chunks.append((length, chunk_type, chunk_content, crc))

    return modified_chunks

def write_png_file(signature, chunks):
    file_path = "out.png"

    with open(file_path, 'wb') as f:
        f.write(signature)

        for length, chunk_type, chunk_content, crc in chunks:
            f.write(length + chunk_type + chunk_content + crc)


file_path = "blank.png"
read_chunks(file_path)

