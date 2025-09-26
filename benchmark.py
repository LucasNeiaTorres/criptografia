import requests
import os
import difflib
import time
import csv

GUTTENBERG_INPUT_URL="https://www.gutenberg.org/cache/epub/10706/pg10706.txt"  # The History of Rome
SIZES = [5_000, 500_000, 5_000_000]

def generate_inputs():
    response = requests.get(GUTTENBERG_INPUT_URL, stream=True)
    dados = b""
    for chunk in response.iter_content(1024): 
        if len(dados) + len(chunk) > 5_000_000:
            dados += chunk[:5_000_000 - len(dados)]
            break
        dados += chunk 
    inputs = []
    for size in SIZES:
        fname = f"input{size}.txt"
        with open(fname, "wb") as f:
            f.write(dados[:size])
        inputs.append(fname)
        print(f"Gerado {fname} com {size} bytes.")
    return inputs

def comparar_arquivos(arq1, arq2):
    with open(arq1, encoding="utf-8") as f1, open(arq2, encoding="utf-8") as f2:
        # strip() remove espaços e quebras de linha no começo/fim
        linhas1 = [linha.rstrip() for linha in f1]
        linhas2 = [linha.rstrip() for linha in f2]

    diff = difflib.ndiff(linhas1, linhas2)
    for line in diff:
        if line.startswith("- "): 
            print(f"< {line[2:]}")
        elif line.startswith("+ "):
            print(f"> {line[2:]}")

def show_table_header(writer):
    writer.writerow(["Arquivo", 
                     "MyCripto Enc (s)", "MyCripto Dec (s)", 
                     "AES Enc (s)", "AES Dec (s)"])

def main():
    inputs = generate_inputs()
    
    with open("resultados.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        show_table_header(writer)
        
        for input in inputs:
            outputEnc = f"{input}.enc.out"
            outputDec = f"{input}.dec.out"
            
            # MyCripto Enc
            cmd1 = f"python3 mycripto.py enc {input} {outputEnc}.mycripto"
            print(f"Executando: {cmd1}")
            start = time.perf_counter()
            os.system(cmd1)
            my_enc_time = time.perf_counter() - start
            
            # AES Enc
            cmd2 = f"python3 criptoAES.py enc {input} {outputEnc}.aes"
            print(f"Executando: {cmd2}")
            start = time.perf_counter()
            os.system(cmd2)
            aes_enc_time = time.perf_counter() - start
            
            # MyCripto Dec
            cmd1 = f"python3 mycripto.py dec {outputEnc}.mycripto {outputDec}.mycripto"
            print(f"Executando: {cmd1}")
            start = time.perf_counter()
            os.system(cmd1)
            my_dec_time = time.perf_counter() - start
            
            # AES Dec
            cmd2 = f"python3 criptoAES.py dec {outputEnc}.aes {outputDec}.aes"
            print(f"Executando: {cmd2}")
            start = time.perf_counter()
            os.system(cmd2)
            aes_dec_time = time.perf_counter() - start
            
            # Comparação
            ok_my = comparar_arquivos(input, f"{outputDec}.mycripto")
            ok_aes = comparar_arquivos(input, f"{outputDec}.aes")
            
            # Salvar linha na tabela
            writer.writerow([input, 
                             f"{my_enc_time:.6f}", f"{my_dec_time:.6f}", 
                             f"{aes_enc_time:.6f}", f"{aes_dec_time:.6f}"])
    
    print("Tabela salva em resultados.csv ✅")
    
if __name__ == "__main__":
    main()