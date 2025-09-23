import sys
from typing import List
# Uso:
#   python mycripto.py enc <arquivo_in> <arquivo_out>
#   python mycripto.py dec <arquivo_in> <arquivo_out>

SHIFT = 10 
KEY = "PROPAROXITONA" 
PAD_CHAR = '_'  

def substitute(char, shift):
    if char.isalpha():
        base = ord('A') if char.isupper() else ord('a')
        return chr((ord(char) - base + shift) % 26 + base)
    return char

def key_to_order(key: str) -> List[int]:
    key_tuples = [(ch, i) for i, ch in enumerate(key)]
    
    sorted_by_char = sorted(key_tuples, key=lambda x: (x[0], x[1]))
    
    order = [0] * len(key)
    for rank, (_, orig_idx) in enumerate(sorted_by_char):
        order[orig_idx] = rank
    return order

def order_to_cols(order: List[int]) -> List[int]:
    cols_by_rank = [None] * len(order)
    for orig_idx, rank in enumerate(order):
        cols_by_rank[rank] = orig_idx
    return cols_by_rank

def transpose(text):
    n = len(KEY)
    rows = (len(text) + n - 1) // n 
    padded_length = rows * n
    padded_text = text.ljust(padded_length, PAD_CHAR)
    
    matrix = [padded_text[i*n:(i+1)*n] for i in range(rows)]
    
    order = key_to_order(KEY)
    cols_by_rank = order_to_cols(order)
    
    encrypted = []
    for rank in range(n):
        col_idx = cols_by_rank[rank]
        for row in matrix:
            encrypted.append(row[col_idx])
    
    return ''.join(encrypted)

def transpose_decrypt(text):
    n = len(KEY)
    rows = (len(text) + n - 1) // n
    order = key_to_order(KEY)              
    cols_by_rank = order_to_cols(order)   

    # Divide o texto em colunas na ordem do ranking
    col_lengths = [rows] * n
    columns = []
    index = 0
    for _ in range(n):
        col_text = text[index:index+rows]
        columns.append(list(col_text))
        index += rows

    # Reorganizar colunas de volta para ordem original
    matrix = []
    for r in range(rows):
        row = [''] * n
        for orig_col, rank in enumerate(order):
            row[orig_col] = columns[rank][r]
        matrix.append(row)

    # Reconstruir texto linha a linha
    decrypted = ''.join(''.join(row) for row in matrix)
    return decrypted.rstrip(PAD_CHAR)



def encrypt(text, shift):
    # primeiro: substituição, depois: transposição
    substituted = ''.join(substitute(c, shift) for c in text)
    encrypted = transpose(substituted)
    return encrypted

def decrypt(text, shift):
    decrypted = transpose_decrypt(text)
    decrypted = ''.join(substitute(c, -shift) for c in decrypted)
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