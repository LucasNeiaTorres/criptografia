import sys
# Uso:
#   python mycripto.py enc <arquivo_in> <arquivo_out>
#   python mycripto.py dec <arquivo_in> <arquivo_out>

# primeiro: substituição, depois: transposição

def substitute(char, shift):
    # if char.isalpha():
    #     base = ord('A') if char.isupper() else ord('a')
    #     return chr((ord(char) - base + shift) % 26 + base)
    # return char
    pass

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
    pass

def encrypt(text, shift):
    pass

def decrypt(text, shift):
    pass

def main():
    if len(sys.argv) != 4 or sys.argv[1] not in {"enc","dec"}:
        print("Uso: python mycripto.py enc|dec arquivo_in arquivo_out")
        sys.exit(1)
    
if __name__ == "__main__":
    main()