# cripto1

## Descrição

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
Para executar o script, use o seguinte comando:

- Para criptografar um arquivo:
```sh
python criptoAES.py enc <arquivo_in> <arquivo_out>
```
- Para descriptografar um arquivo:
```sh
python criptoAES.py dec <arquivo_in> <arquivo_out>
```

