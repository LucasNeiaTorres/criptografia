import sys
# Uso:
#   python mycripto.py enc <arquivo_in> <arquivo_out>
#   python mycripto.py dec <arquivo_in> <arquivo_out>

# primeiro: substituição, depois: transposição

SHIFT = 3  
KEY = "LUA"  # chave para a transposição

def substitute(char, shift):
    if char.isalpha():
        base = ord('A') if char.isupper() else ord('a')
        return chr((ord(char) - base + shift) % 26 + base)
    return char

# Funcionamento da transposição:
# Texto: ATAQUENORTE
# Chave: LUA (ordem alfabética: A=1, L=2, U=3)

# L   U   A
# ----------
# A   T   A
# Q   U   E
# N   O   R
# T   E   X   (X = letra de enchimento)

# A = 1ª, L = 2ª, U = 3ª

# Coluna A: A E R X
# Coluna L: A Q N T
# Coluna U: T U O E

# Texto cifrado: AERXAQNTTUOE

def transpose(text):
    transposed = text
    
    return transposed

def encrypt(text, shift):
    substituted = ''.join(substitute(c, shift) for c in text)
    encrypted = transpose(substituted)
    return encrypted

def decrypt(text, shift):
    decrypted = ''.join(substitute(c, -shift) for c in text)
    # decrypted = transpose(substituted)
    return decrypted

def encrypt_file(fin, fout):
    text = open(fin, encoding="utf-8").read()
    encrypted_text = encrypt(text, SHIFT)
    with open(fout, "w") as f:
        f.write(encrypted_text)

def decrypt_file(fin, fout):
    text = open(fin, encoding="utf-8").read()
    decrypted_text = decrypt(text, SHIFT)
    with open(fout, "w") as f:
        f.write(decrypted_text)

def main():
    if len(sys.argv) != 4 or sys.argv[1] not in {"enc","dec"}:
        print("Uso: python mycripto.py enc|dec arquivo_in arquivo_out")
        sys.exit(1)
        
    mode, fin, fout = sys.argv[1:]
    
    if mode == "enc":
        encrypt_file(fin, fout)
        print(f"Arquivo {fin} -> {fout} (cifrado).")
    else:
        decrypt_file(fin, fout)
        print(f"Arquivo {fin} -> {fout} (decifrado).")
    
if __name__ == "__main__":
    main()