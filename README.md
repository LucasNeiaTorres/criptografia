# criptografia

Duas cifras de arquivo em Python, lado a lado, para comparar o que se aprende
escrevendo uma cifra do zero com o que se ganha usando uma de verdade:

- **MyCripto** — cifra clássica escrita à mão, combinando **substituição**
  (César de deslocamento fixo) com **transposição colunar por chave**.
- **AES** — AES-256 em modo **GCM**, chamado através da biblioteca
  [`cryptography`](https://cryptography.io) (que por baixo usa o OpenSSL).
  Aqui não há algoritmo escrito por mim: o valor está em usar a primitiva certa.

E um terceiro programa que mede as duas em arquivos de 5 KB, 500 KB e 5 MB e
gera CSV e gráficos comparativos.

---

## ⚠️ Isto é código didático. Não proteja nada real com ele.

**O MyCripto não protege nada.** Ele é uma cifra clássica do século XIX: quem
tem o texto cifrado e um pouco de paciência recupera o texto claro com análise
de frequência, porque a substituição é um César de deslocamento fixo e a
transposição não muda a contagem de letras. Além disso a chave está escrita
dentro do código-fonte, neste repositório público — o que dispensa até a
criptanálise.

**O lado AES também não deve ser usado para proteger nada de verdade**, e o
motivo é mais importante que o anterior: implementação caseira de criptografia é
insegura por construção, mesmo quando o algoritmo está matematicamente correto e
mesmo quando a primitiva vem de uma biblioteca séria. Faltam aqui, entre outras
coisas:

- **gestão de chave** — a chave AES-256 é gravada em hexadecimal, em texto
  puro, num arquivo `aes_key.hex` no diretório de trabalho, sem senha, sem
  derivação a partir de senha (KDF), sem permissão restrita e sem qualquer
  rotação;
- **cuidado com canal lateral** — o MyCripto processa caractere a caractere em
  Python, com tempo dependente do conteúdo, e nada aqui foi pensado para
  resistir a medição de tempo ou de memória;
- **revisão independente** — nada disto foi auditado por ninguém, e código de
  criptografia é justamente a categoria em que "parece funcionar" não tem
  qualquer relação com "está seguro";
- **tratamento de erro de decifragem** — o `AESGCM.decrypt` levanta exceção
  quando a autenticação falha, e o programa simplesmente estoura com um
  *traceback*, sem distinguir "arquivo adulterado" de "chave errada".

Para proteger arquivo de verdade use ferramenta pronta e revisada (`age`, GnuPG,
`openssl enc` com uma configuração conhecida, ou a `cryptography` chamada dentro
de um desenho de sistema que alguém revisou). Este repositório existe para
**entender**, não para **usar**.

---

## Contexto: por que isto existe

É um trabalho acadêmico, e o enunciado por trás dele é o clássico da área:
implemente uma cifra sua, implemente (ou chame) uma cifra moderna, e compare.
O objetivo do exercício não é produzir algo utilizável — é sentir na mão a
distância entre as duas coisas.

O que ele acaba mostrando bem, e que não estava no enunciado, é uma lição
diferente: **a cifra escrita à mão não falhou por ser fraca, falhou por ser
errada.** Ela corrompe silenciosamente qualquer texto com acento (veja
[Limitações conhecidas](#limitações-conhecidas-e-bugs)). O AES nunca teve esse
problema, não porque o AES seja mais esperto, mas porque ele opera sobre
**bytes** e a implementação caseira caiu na tentação de operar sobre
**caracteres**.

---

## O que está de fato implementado

| Programa | O que faz | Escrito do zero? |
|---|---|---|
| `mycripto.py` | Substituição de César (`SHIFT = 10`) seguida de transposição colunar com a chave `VQJYRMZTKLHP`, sobre arquivo de texto | **Sim** — inclusive a permutação de colunas e o preenchimento |
| `criptoAES.py` | AES-256-GCM sobre arquivo binário; gera e persiste a chave; prefixa o *nonce* de 12 bytes ao texto cifrado | Não — usa `cryptography.hazmat.primitives.ciphers.aead.AESGCM` |
| `benchmark.py` | Baixa um texto do Projeto Gutenberg, recorta em 5 KB / 500 KB / 5 MB, roda os dois programas, cronometra, grava CSV e desenha os gráficos | Sim |

**Não há** aqui RSA, Diffie-Hellman, aritmética modular de números grandes,
geração ou teste de primalidade, nem nenhum ataque implementado (força bruta ou
análise de frequência). O repositório é sobre cifra simétrica de arquivo, só.

---

## A decisão difícil: a transposição colunar

O César é trivial — uma linha de aritmética modular. A parte que exigiu pensar
foi a transposição, e especificamente **manter duas permutações que são inversas
uma da outra sem confundi-las**, que é onde esse algoritmo costuma quebrar.

A ideia da transposição colunar é: escreva o texto numa matriz de `len(chave)`
colunas e leia as colunas **na ordem alfabética das letras da chave**. Com a
chave `LUA` e o texto `ATAQUENORTE`:

```
L   U   A          ordem alfabética:  A=1º, L=2º, U=3º
---------
A   T   A
Q   U   E
N   O   R
T   E   _          '_' = caractere de enchimento
```

Lendo a coluna `A`, depois a `L`, depois a `U`: `AER_` + `AQNT` + `TUOE` =
`AER_AQNTTUOE`. (Este resultado foi conferido rodando o próprio código com
`KEY = "LUA"`.)

O detalhe que dá trabalho é que existem **dois índices diferentes** para a mesma
coluna e é fácil trocá-los:

- `key_to_order(key)` devolve, para cada coluna **na posição original**, qual é o
  seu **posto** na ordem alfabética. Para a chave real deste projeto,
  `VQJYRMZTKLHP` → `[9, 6, 1, 10, 7, 4, 11, 8, 2, 3, 0, 5]`: a coluna 0 (o `V`)
  é a 9ª a ser lida, a coluna 10 (o `H`) é a primeira.
- `order_to_cols(order)` inverte essa lista: para cada **posto**, qual coluna
  original ocupá-lo.

Cifrar usa a segunda ("para cada posto, pegue a coluna"); decifrar usa a
primeira ("cada bloco lido é o posto *r*; devolva-o à sua coluna original").
Escrever só uma das duas e tentar reusá-la nos dois sentidos é o erro clássico —
funciona para chaves cujo alfabeto é quase ordenado e falha para as outras, o
que é o pior tipo de bug, porque passa no primeiro teste.

Um segundo cuidado: o desempate. A ordenação é feita por `(letra, índice
original)`, então **chave com letras repetidas continua produzindo uma
permutação determinística e reversível** — sem isso, chave como `CASA` daria
resultados dependentes da estabilidade do `sorted`.

O terceiro é o **enchimento**. O texto é completado com `_` até fechar a última
linha, e a decifragem remove os `_` do fim. É uma solução simples que tem um
preço, assumido e documentado abaixo: texto claro que legitimamente termina em
`_` perde esses caracteres. Um esquema de *padding* de verdade (PKCS#7, por
exemplo) codifica **quantos** bytes foram acrescentados justamente para não ter
essa ambiguidade.

---

## O lado AES: o que vale reparar

São 60 linhas, e quase toda a decisão está em **qual** primitiva chamar:

- **GCM, não ECB nem CBC.** GCM é um modo autenticado (AEAD): além de cifrar,
  produz uma etiqueta que faz a decifragem **falhar** se o arquivo tiver sido
  alterado. Cifrar sem autenticar deixa o texto cifrado silenciosamente
  maleável.
- **Um *nonce* aleatório de 12 bytes por arquivo**, gerado com `os.urandom` e
  **gravado como prefixo do arquivo cifrado** — daí a decifragem começar com
  `data[:12], data[12:]`. Nonce repetido com a mesma chave é a falha fatal do
  GCM, e é por isso que ele é sorteado a cada execução em vez de ser fixo.
- **Modo binário em todo o caminho** (`open(..., "rb")` / `"wb"`). Foi
  exatamente isso que a cifra caseira não fez, e é a origem do bug de acentos.

O arquivo cifrado é, portanto: `nonce (12 bytes) || texto cifrado || etiqueta
GCM (16 bytes)` — 28 bytes maiores que a entrada.

---

## Como rodar

Requisitos: Python 3.8 ou superior e `pip`.

```sh
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### MyCripto

```sh
python3 mycripto.py enc in.txt out.txt
python3 mycripto.py dec out.txt   volta.txt
```

A chave e o deslocamento estão fixos no topo do `mycripto.py` (`SHIFT`, `KEY`) —
mudá-los é editar o arquivo.

### AES

```sh
python3 criptoAES.py enc in.txt out.enc
python3 criptoAES.py dec out.enc  volta.txt
```

Na primeira execução o programa **gera** uma chave AES-256 e a grava em
`aes_key.hex`, no diretório atual. Sem esse arquivo, o que foi cifrado não volta
mais — e com esse arquivo, qualquer um decifra. Leia o aviso lá em cima.

### Benchmark

```sh
python3 benchmark.py
```

Ele baixa *The History of Rome* do Projeto Gutenberg, recorta em três tamanhos,
roda os quatro comandos (cifrar e decifrar, nos dois algoritmos), imprime o
`diff` entre o original e o texto recuperado, e produz:

- `resultados.csv` — os tempos;
- `comparacao_enc.png` e `comparacao_dec.png` — os gráficos de barras.

**Cuidado ao ler esses números.** Cada medição envolve `os.system("python3 …")`,
ou seja, cronometra **o processo inteiro**: subir o interpretador, importar
módulos, ler o arquivo, cifrar e escrever. No caso de 5 KB isso é quase só
partida do interpretador, e a diferença entre os dois algoritmos fica enterrada
no ruído. Os números só começam a dizer algo sobre os algoritmos no arquivo de
5 MB. Uma versão honesta mediria dentro do processo, em volta apenas da chamada
de cifragem, e repetiria cada medição algumas vezes.

Nenhum resultado está versionado neste repositório — os CSV e PNG citados são
produzidos na sua máquina, e este README não afirma qualquer número.

---

## Limitações conhecidas e bugs

Estes foram verificados rodando o código, não deduzidos:

- **🔴 O MyCripto corrompe texto acentuado, em silêncio.** `'ç'.isalpha()` é
  `True` em Python, então o César tenta deslocar o caractere; mas
  `(ord('ç') - ord('a') + 10) % 26 + ord('a')` joga o resultado de volta na
  faixa ASCII, e o deslocamento inverso não tem como saber de onde ele veio.
  Na prática: `acentuação e ç` cifra e decifra de volta como `acentuaeao e e`.
  A cifra não é bijetora fora de `[A-Za-z]`. O conserto é operar sobre bytes,
  ou restringir o deslocamento a `A-Z`/`a-z` verificando a faixa em vez de
  chamar `isalpha()`.
- **Texto claro terminado em `_` perde esses caracteres.** A decifragem faz
  `rstrip('_')` para remover o enchimento e não distingue enchimento de
  conteúdo. Verificado: `termina com underline___` volta como
  `termina com underline`.
- **O MyCripto lê em UTF-8 e escreve na codificação padrão do sistema.** A
  leitura é `open(fin, encoding="utf-8")`, a escrita é `open(fout, "w")` sem
  `encoding` — em máquina cuja localidade não seja UTF-8, o par não fecha.
- **O `benchmark.py` recorta o texto por contagem de *bytes*** e depois o
  MyCripto o lê como UTF-8; se o corte cair no meio de um caractere de vários
  bytes, a leitura levanta `UnicodeDecodeError`. Com um texto em inglês quase
  todo ASCII o problema não costuma aparecer, mas ele está lá.
- **A conferência do benchmark não confere nada.** `compare_files()` imprime as
  diferenças mas não devolve valor; as variáveis `ok_my` e `ok_aes` recebem
  `None` e nunca são usadas. O benchmark não falha quando um algoritmo devolve
  texto errado — e, pelo bug de acentos, ele pode devolver.
- **O `.gitignore` tem um erro de digitação: ignora `aes_hey.hex`**, e o arquivo
  de chave que o programa cria chama-se `aes_key.hex`. Ou seja, a chave gerada
  **não** está protegida contra um `git add .` distraído. (Conferido: nenhuma
  chave foi de fato versionada até hoje. Mas a rede de proteção não existe.)
- **A decifragem do MyCripto assume entrada bem-formada.** Texto cifrado cujo
  comprimento não seja múltiplo do tamanho da chave produz lixo ou estoura, sem
  mensagem útil.
- **Sem testes automatizados.** Tudo acima foi descoberto executando o código à
  mão; um punhado de testes de ida-e-volta com entradas adversariais (acento,
  vazio, terminando em `_`, exatamente do tamanho da chave) teria pego os dois
  primeiros itens.

---

## Estrutura

```
.
├── mycripto.py        cifra clássica escrita à mão: César + transposição colunar
├── criptoAES.py       AES-256-GCM via biblioteca cryptography
├── benchmark.py       gera as entradas, cronometra os dois, escreve CSV e gráficos
├── requirements.txt   cryptography, pandas, matplotlib, requests
├── in.txt             arquivo de entrada mínimo, para teste rápido
└── .gitignore
```
