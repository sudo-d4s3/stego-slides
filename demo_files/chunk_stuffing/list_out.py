#!/usr/bin/env python3
import os

def read_chunks(file_path):
    with open(file_path, 'rb') as f:
        f.seek(0,os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        signature = f.read(8)
        print(f"Signature: {signature}")


        while True:
            if f.tell() >= file_length:
                break

            length = f.read(4)
            chunk_type = f.read(4)
            chunk_content = f.read(int(length.hex(),16))
            crc = f.read(4)

            print(f"\nChunk Type: {chunk_type.decode()}")
            print(f"Size: {int(length.hex(),16)}")
            print(f"CRC: {crc.hex()}")

file_path = "out.png"
read_chunks(file_path)
