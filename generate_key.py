# generate_key.py
import os

key = os.urandom(32)  # 32 bytes = 256 bits
with open("aes_key.hex", "w") as f:
    f.write(key.hex())

print("Chave AES-256 salva em aes_key.hex")
