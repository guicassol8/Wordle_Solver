# Wordle Solver

Projeto pessoal desenvolvido por **Guilherme Roth Cassol** para resolver automaticamente o jogo **Wordle** de 5 letras.  
A solução utiliza **Python + Selenium** para automatizar o jogo e um **frontend em React**.

O objetivo principal do projeto é demonstrar a **lógica utilizada para resolver o Wordle**, utilizando heurísticas baseadas em frequência de letras e filtragem progressiva do dicionário.

O código Python **não foi escrito com foco em boas práticas ou arquitetura**, pois foi criado como um projeto pessoal experimental. Mesmo assim, a lógica utilizada é eficiente e o algoritmo possui uma taxa de acerto muito alta.

---

# Como rodar o projeto

## 1. Rodar o frontend

Entre na pasta do frontend e instale as dependências:

```bash
npm i
```

Depois execute o servidor de desenvolvimento:

```bash
npm run dev
```

---

## 2. Rodar o solver em Python

Após iniciar o frontend, rode o script Python responsável por resolver o jogo automaticamente:

```bash
uv run main.py
```

---

# Controle de velocidade do solver

A velocidade de execução do bot é controlada diretamente no código Python através de chamadas para:

```python
time.sleep(...)
```

Caso queira:

- **Acelerar a solução:** diminua o valor do `sleep`
- **Diminuir a velocidade:** aumente o valor do `sleep`

Isso apenas controla o intervalo entre ações do Selenium no navegador.

---

# Como o algoritmo funciona

A seguir está uma explicação simplificada da estratégia utilizada pelo solver.

## 1. Mapeamento de frequência de letras

Inicialmente o código percorre todas as palavras disponíveis no dicionário.

Ele utiliza:

- o dicionário principal
- o arquivo `adicao.txt` (palavras que existem no site mas não estão no dicionário base)

Para cada palavra, o algoritmo incrementa a frequência de cada letra em um **mapa de letras**, onde:

```
chave = letra
valor = número de ocorrências
```

Com esse mapa é possível atribuir um **score para cada palavra**, indicando o quão boa ela é para cobrir o maior número possível de letras comuns.

---

## 2. Primeiro chute

O primeiro chute sempre é:

```
soare
```

Essa palavra foi escolhida pois possui o **maior score baseado na frequência de letras**, sendo uma excelente palavra inicial para coletar informação.

---

## 3. Interpretação das cores

Após o chute, o Wordle retorna informações através das cores:

- **Verde:** letra correta na posição correta
- **Amarelo:** letra existe, mas na posição errada
- **Cinza:** letra não existe na palavra

O algoritmo interpreta essas informações e atualiza um conjunto de regras, como:

- posições fixas de letras (verdes)
- posições proibidas para certas letras (amarelas)
- letras que não podem aparecer (cinza)

Também existem otimizações extras, como tratar corretamente **letras repetidas**, por exemplo:

- quando uma letra aparece duas vezes
- uma ocorrência é cinza e outra amarela

Isso permite deduzir **quantidade máxima de uma letra na palavra**.

---

## 4. Filtragem do dicionário

Com as regras obtidas, o algoritmo percorre o dicionário e remove todas as palavras que:

- não respeitam as posições verdes
- usam letras proibidas
- colocam letras amarelas nas posições erradas
- violam restrições de repetição

O resultado é um **dicionário reduzido contendo apenas palavras possíveis**.

Outro detalhe: palavras com **letras repetidas recebem menor prioridade**, pois geralmente fornecem menos informação.

---

## 5. Recalcular score das palavras

Depois da filtragem, o algoritmo:

1. Recalcula o **mapa de frequência das letras** usando apenas as palavras restantes.
2. Recalcula o **score das palavras** baseado nesse novo mapa.

Isso permite priorizar palavras que maximizam a descoberta de novas letras.

---

## 6. Escolha da próxima palavra

O algoritmo mantém dois conjuntos:

- **dicionário filtrado** (palavras possíveis)
- **dicionário completo ordenado por score**

A palavra escolhida normalmente é a que possui **maior score**, pois ela maximiza a quantidade de informação obtida no próximo chute.

---

## 7. Loop até vitória

Com a nova palavra escolhida:

1. o bot faz o chute
2. interpreta as cores
3. filtra o dicionário
4. escolhe uma nova palavra

Esse processo se repete até que todas as letras estejam **verdes**, indicando que a palavra foi descoberta.

---

# Possíveis melhorias

Uma melhoria interessante que poderia ser implementada seria considerar também a **frequência das letras por posição**.

Exemplo:

- qual letra aparece mais frequentemente na posição 1
- qual letra aparece mais na posição 5

Essa heurística poderia melhorar ainda mais a eficiência do algoritmo.

No entanto, a solução atual já possui **performance quase perfeita**, raramente errando a palavra.

---

# Autor

Projeto desenvolvido por:

**Guilherme Roth Cassol**
