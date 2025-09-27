# cripto1

## Descrição

Este trabalho implementa dois algoritmos de criptografia em Python:  
- **MyCripto**: algoritmo próprio que combina substituição (Caesar com shift fixo) e transposição (com chave definida).  
- **AES**: implementado em Python utilizando a biblioteca [`cryptography`](https://cryptography.io), que fornece acesso seguro às funções do OpenSSL.  

Além disso, foi desenvolvido um script de **benchmark** que compara o desempenho (tempo de encriptação e decriptação) entre o MyCripto e o AES em diferentes tamanhos de entrada.


<!-- # Funcionamento da transposição:
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

# Texto cifrado: AERXAQNTTUOE -->

## Pré-requisitos
Certifique-se de ter o seguinte instalado em seu sistema:
- Python 3.8 ou superior
- `pip` para gerenciar pacotes Python

## Configuração do Ambiente

1. **Clone o repositório**:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd cripto1
    ```
2. **Crie o ambiente virtual**:
   ```sh
   python3 -m venv venv
   ```

3. **Ative o ambiente virtual**:
    - No Windows:
      ```sh
      venv\Scripts\activate
      ```
    - No Linux/Mac:
      ```sh
      source venv/bin/activate
      ```

4. **Instale as dependências**:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### AES
- Para criptografar um arquivo:
```sh
python criptoAES.py enc <arquivo_in> <arquivo_out>
```
- Para descriptografar um arquivo:
```sh
python criptoAES.py dec <arquivo_in> <arquivo_out>
```

### MyCripto
- Para criptografar um arquivo:
```sh
python mycripto.py enc <arquivo_in> <arquivo_out>
```
- Para descriptografar um arquivo:
```sh
python mycripto.py dec <arquivo_in> <arquivo_out>
```

## Benchmark
O script de benchmark baixa automaticamente um texto do Projeto Gutenberg e gera arquivos de entrada com tamanhos de 5 KB, 500 KB e 5 MB.
Ele executa os dois algoritmos (MyCripto e AES), mede os tempos de execução e salva os resultados em um arquivo CSV, além de gerar gráficos comparativos.

Para executar o benchmark, use o seguinte comando:
```sh
python benchmark.py
```

Os resultados serão gerados em:
- `resultados.csv`: arquivo CSV com os tempos de execução.
- `comparacao_desc.png`: gráfico comparativo dos tempos de descriptografia.
- `comparacao_enc.png`: gráfico comparativo dos tempos de criptografia.