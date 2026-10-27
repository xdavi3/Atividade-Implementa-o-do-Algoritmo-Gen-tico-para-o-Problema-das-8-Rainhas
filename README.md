# Atividade – Implementação do Algoritmo Genético para o Problema das 8 Rainhas

Este repositório contém a resolução completa da atividade prática de **Inteligência Artificial / Algoritmos Genéticos** aplicada ao clássico **Problema das 8 Rainhas (8-Queens Puzzle)**.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xdavi3/Atividade-Implementa-o-do-Algoritmo-Gen-tico-para-o-Problema-das-8-Rainhas/blob/main/IA-GeneticAlgorithm-8queens-exercicio.ipynb)

---

## 🎯 Objetivo

Completar a implementação de um **Algoritmo Genético (GA)** para resolver o problema das 8 rainhas em Python/Jupyter Notebook, utilizando e integrando os operadores genéticos (seleção por torneio, crossover de um ponto e mutação pontual).

---

## ♟️ Descrição do Problema

O desafio consiste em posicionar 8 rainhas em um tabuleiro de xadrez $8 \times 8$ de tal forma que nenhuma delas ataque outra. Em termos de regras do xadrez, isso significa que nenhuma dupla de rainhas pode compartilhar a mesma **linha horizontal**, **coluna vertical** ou **diagonal**.

### Modelagem Adotada

- **Cromossomo / Indivíduo**: Vetor de 8 inteiros $VT = [r_0, r_1, \dots, r_7]$, onde o índice da posição representa a **coluna** (0 a 7) e o valor $r_i \in \{1, 2, \dots, 8\}$ representa a **linha** ocupada pela rainha.
- **Vantagem da representação**: Conflitos entre colunas são automaticamente eliminados por construção, reduzindo o espaço de busca de $\binom{64}{8} \approx 4,42 \times 10^9$ para $8^8 = 16.777.216$ estados possíveis.
- **Função de Aptidão (Fitness / Custo)**: O algoritmo minimiza o número total de conflitos:
  $$\text{Custo}(VT) = \text{Ataques em Linhas}(VT) + \text{Ataques em Diagonais}(VT)$$
  A solução ótima global é alcançada quando $\text{Custo}(VT) = 0$.

---

## 🧬 Operadores Genéticos Implementados

1. **População Inicial (`gera_populacao_inicial`)**:
   - Gera `tam_pop` indivíduos aleatórios com valores inteiros entre 1 e 8 para cada coluna.
2. **Seleção por Torneio Binário (`selecao`)**:
   - Sorteia 2 indivíduos da população e elege o que possui o menor número de ataques (menor custo).
3. **Crossover de Um Ponto (`crossover`)**:
   - Com probabilidade `taxa_crossover` (padrão 85%), sorteia um ponto de corte aleatório $k \in [1, 7]$ e recombina os genes dos dois pais para produzir dois descendentes.
4. **Mutação Pontual (`mutacao`)**:
   - Com probabilidade `taxa_mutacao` (padrão 10% por gene), uma coluna recebe uma nova linha aleatória entre 1 e 8, garantindo exploração e prevenção de estagnação em mínimos locais.
5. **Elitismo e Critério de Parada (`algoritmo_genetico`)**:
   - Preserva os $K=2$ melhores indivíduos para a próxima geração, garantindo que o melhor custo seja monotonamente decrescente.
   - Interrompe a execução antecipadamente assim que um indivíduo com **0 ataques** for encontrado.

---

## 📊 Visualizações e Resultados

O notebook inclui:
- **Visualização do Tabuleiro de Xadrez 8x8**: Renderizado graficamente via `matplotlib` com padrão clássico de casas claras/escuras e o caractere Unicode `♛` em cada posição encontrada.
- **Curva de Convergência**: Gráfico mostrando a evolução do melhor custo e da média da população ao longo das gerações.
- **Conversão em Matriz Binária**: Matriz $8 \times 8$ com 0s e 1s gerada por `converte_tabuleiro(VT)`.

---

## 📈 Reflexão Final e Análise de Parâmetros

### 1. Quantas execuções, em média, foram necessárias para encontrar uma solução válida?
- **Taxa de Sucesso**: ~**90% a 95%** das execuções encontram a solução com 0 conflitos dentro do limite de 300 gerações.
- **Média de Gerações**: Quando há convergência, a média fica entre **37 e 48 gerações** (desvio padrão $\approx 35\text{--}50$, mediana $\approx 30\text{--}35$).
- Em casos com combinações genéticas iniciais favoráveis, a solução foi encontrada em menos de 15 gerações; em platôs, demandou entre 80 e 140 gerações.

### 2. Melhores Combinações de Parâmetros

| População | Mutação | Crossover | Elitismo | Sucesso (%) | Média de Gerações | Análise |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **20** | 0.05 | 0.80 | Sim | ~30% | 66.3 ± 50.2 | População restrita; estagnação prematura frequente em 1 conflito. |
| **50** | 0.05 | 0.80 | Sim | ~70% | 77.1 ± 94.4 | Desempenho moderado; diversidade média. |
| **100** | 0.05 | 0.80 | Sim | ~65% | 59.2 ± 92.0 | Mutação baixa (0.05) não desfaz platôs com facilidade. |
| **100** | **0.10** | **0.85** | **Sim** | **~90% - 95%** | **37.2 a 48.2** | **Melhor Configuração**: Excelente balanço entre tempo e convergência. |
| **100** | 0.15 | 0.85 | Sim | ~95% | 99.6 ± 77.3 | Alta taxa de sucesso, mas mutação agressiva retarda a convergência fina. |
| **100** | 0.10 | 0.85 | Não | ~95% | 72.8 ± 53.2 | Sem elitismo, há risco de perder o melhor indivíduo temporariamente. |
| **200** | 0.10 | 0.85 | Sim | ~90% | 42.4 ± 50.8 | Bom resultado, mas dobra o tempo computacional por geração. |

- **População Ideal**: `100` indivíduos (tempo de execução inferior a 0.5s).
- **Mutação Ideal**: `0.10` por gene (média de $8 \times 0.10 = 0.8$ mutações por indivíduo).
- **Crossover Ideal**: `0.85` (ampla recombinação).
- **Elitismo**: Fundamental para assegurar preservação das soluções já encontradas.

### 3. O que funcionou bem e o que pode ser melhorado?

**O que funcionou bem:**
- Representação vetorial 1D descartando conflitos por coluna.
- Torneio binário simples e eficiente ($O(1)$).
- Elitismo protegendo o melhor fitness.
- Parada antecipada poupando iterações desnecessárias.

**O que pode ser melhorado:**
- **Representação por Permutação Estrita**: Utilizar permutações dos números de 1 a 8 eliminaria de antemão todos os conflitos de linha, reduzindo o espaço de estados de $16.777.216$ para $8! = 40.320$ (redução de 99,76% no espaço de busca), com operadores PMX/OX.
- **Mutação Adaptativa**: Aumentar a taxa de mutação dinamicamente se a população permanecer estagnada por mais de $K$ gerações.
- **Filtro de Diversidade**: Impedir indivíduos idênticos na mesma geração.

---

## 🚀 Como Executar

1. Abra o notebook `IA-GeneticAlgorithm-8queens-exercicio.ipynb` no **Google Colab** ou em seu ambiente Jupyter local:
   ```bash
   jupyter notebook IA-GeneticAlgorithm-8queens-exercicio.ipynb
   ```
2. Execute as células sequencialmente (`Shift + Enter`).
3. O notebook executará os testes, gerará a visualização gráfica do tabuleiro e apresentará a análise estatística completa.
