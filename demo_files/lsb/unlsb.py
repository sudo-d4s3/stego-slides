#!/usr/bin/env python3
import os

def extract_hidden_text(file_path):
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

        binary_message = ''

        for length, chunk_type, chunk_content, crc in chunks:
            if chunk_type == b'IDAT':
                for byte in chunk_content:
                    binary_byte = format(byte, '08b')
                    binary_message += binary_byte[-1]

        extracted_text = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        return extracted_text

file_path = "out.png"
hidden_text = extract_hidden_text(file_path)
print(f"Extracted Hidden Text: {hidden_text}")
