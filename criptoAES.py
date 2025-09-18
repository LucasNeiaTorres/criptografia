import os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Uso:
#   python criptoAES.py enc <arquivo_in> <arquivo_out>
#   python criptoAES.py dec <arquivo_in> <arquivo_out>

KEY_FILE = "aes_key.hex"
    
def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            key_hex = f.read().strip()
            try:
                key = bytes.fromhex(key_hex)
                if len(key) not in (16, 24, 32):
                    raise ValueError("Tamanho inválido da chave.")
                return key
            except Exception:
                print("Arquivo de chave corrompido. Gerando nova chave...")

    key = os.urandom(32)  # 32 bytes = 256 bits (AES-256)
    with open(KEY_FILE, "w") as f:
        f.write(key.hex())
    print(f"Nova chave AES-256 gerada e salva em {KEY_FILE}")
    return key

def encrypt_file(fin, fout, key):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    plaintext = open(fin, "rb").read()
    ct = aes.encrypt(nonce, plaintext, None)
    with open(fout, "wb") as f:
        f.write(nonce + ct)

def decrypt_file(fin, fout, key):
    data = open(fin, "rb").read()
    nonce, ct = data[:12], data[12:]
    aes = AESGCM(key)
    pt = aes.decrypt(nonce, ct, None)
    with open(fout, "wb") as f:
        f.write(pt)

def main():
    if len(sys.argv) != 4 or sys.argv[1] not in {"enc","dec"}:
        print("Uso: python criptoAES.py enc|dec arquivo_in arquivo_out")
        sys.exit(1)

    mode, fin, fout = sys.argv[1:]
    key = load_or_create_key()

    if mode == "enc":
        encrypt_file(fin, fout, key)
        print(f"Arquivo {fin} -> {fout} (cifrado).")
    else:
        decrypt_file(fin, fout, key)
        print(f"Arquivo {fin} -> {fout} (decifrado).")

if __name__ == "__main__":
    main()