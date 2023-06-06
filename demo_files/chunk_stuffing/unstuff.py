#!/usr/bin/env python3
import os

def read_chunks(file_path):
    with open(file_path, 'rb') as f:
        f.seek(0,os.SEEK_END)
        file_length = f.tell()
        f.seek(0)
        signature = f.read(8)
        #print(f"Signature: {signature}")


        while True:
            if f.tell() >= file_length:
                break

            length = f.read(4)
            chunk_type = f.read(4)
            chunk_content = f.read(int(length.hex(),16))
            crc = f.read(4)

            if chunk_type == b'stEg':
                with open(extracted_chunk, 'wb') as exf:
                    exf.write(chunk_content)

file_path = "out.png"
extracted_chunk = "out_chunk"
read_chunks(file_path)
