import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
import difflib
import time
import csv

GUTTENBERG_INPUT_URL="https://www.gutenberg.org/cache/epub/10706/pg10706.txt"  # The History of Rome
SIZES = [5_000, 500_000, 5_000_000]
CSV_FILE = "resultados.csv"

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

def compare_files(arq1, arq2):
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

def generate_graph(csv_file):   
    df = pd.read_csv(csv_file)

    # --- Gráfico de ENCRIPTAÇÃO ---
    plt.figure(figsize=(10, 6))
    x = range(len(df["Tamanho (bytes)"]))
    width = 0.35

    plt.bar([i - width/2 for i in x], df["MyCripto Enc (s)"], width=width, label="MyCripto Enc")
    plt.bar([i + width/2 for i in x], df["AES Enc (s)"], width=width, label="AES Enc")

    plt.xticks(x, df["Tamanho (bytes)"], rotation=45)
    plt.xlabel("Tamanho (bytes)")
    plt.ylabel("Tempo (segundos)")
    plt.title("Comparação de Tempo - Encriptação")
    plt.legend()
    plt.savefig("comparacao_enc.png", dpi=300, bbox_inches="tight")
    plt.show()

    # --- Gráfico de DECRIPTAÇÃO ---
    plt.figure(figsize=(10, 6))
    plt.bar([i - width/2 for i in x], df["MyCripto Dec (s)"], width=width, label="MyCripto Dec")
    plt.bar([i + width/2 for i in x], df["AES Dec (s)"], width=width, label="AES Dec")

    plt.xticks(x, df["Tamanho (bytes)"], rotation=45)
    plt.xlabel("Tamanho (bytes)")
    plt.ylabel("Tempo (segundos)")
    plt.title("Comparação de Tempo - Decriptação")
    plt.legend()
    plt.savefig("comparacao_dec.png", dpi=300, bbox_inches="tight")


def show_table_header(writer):
    writer.writerow(["Tamanho (bytes)", 
                     "MyCripto Enc (s)", "MyCripto Dec (s)", 
                     "AES Enc (s)", "AES Dec (s)"])

def main():
    inputs = generate_inputs()
    
    with open(CSV_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        show_table_header(writer)
        
        for indice, input in enumerate(inputs):
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
            ok_my = compare_files(input, f"{outputDec}.mycripto")
            ok_aes = compare_files(input, f"{outputDec}.aes")
            
            # Salvar linha na tabela
            writer.writerow([SIZES[indice], 
                             f"{my_enc_time:.6f}", f"{my_dec_time:.6f}", 
                             f"{aes_enc_time:.6f}", f"{aes_dec_time:.6f}"])
    
    print("Tabela salva em", CSV_FILE)  
    
    generate_graph(CSV_FILE)
    
if __name__ == "__main__":
    main()