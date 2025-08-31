# cripto1

## Descrição

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