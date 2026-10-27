"""
Script Executável - Algoritmo Genético para o Problema das 8 Rainhas
Autor: David de Assis
"""

import random
import time
import numpy as np
import matplotlib.pyplot as plt

def converte_tabuleiro(VT):
    N = len(VT)
    T = [[0] * N for _ in range(N)]
    for col in range(N):
        lin = VT[col] - 1
        T[lin][col] = 1
    return T

def __conta_ataques_linhas(VT):
    ataques = 0
    N = len(VT)
    for c1 in range(N):
        l1 = VT[c1]
        for c2 in range(c1 + 1, N):
            if l1 == VT[c2]:
                ataques += 1
    return ataques

def __conta_ataques_diagonais(VT):
    ataques = 0
    N = len(VT)
    for c1 in range(N):
        l1 = VT[c1]
        for c2 in range(c1 + 1, N):
            l2 = VT[c2]
            if abs(l1 - l2) == abs(c1 - c2):
                ataques += 1
    return ataques

def conta_ataques(VT):
    return __conta_ataques_linhas(VT) + __conta_ataques_diagonais(VT)

def gera_individuo(n_cols):
    return np.random.randint(low=1, high=n_cols + 1, size=n_cols)

def gera_populacao_inicial(N, tam_pop):
    return [gera_individuo(N) for _ in range(tam_pop)]

def selecao(Populacao):
    c1 = random.choice(Populacao)
    c2 = random.choice(Populacao)
    return c1 if conta_ataques(c1) <= conta_ataques(c2) else c2

def crossover(pai1, pai2, taxa_crossover=0.85):
    if random.random() < taxa_crossover:
        ponto = random.randint(1, len(pai1) - 1)
        f1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
        f2 = np.concatenate((pai2[:ponto], pai1[ponto:]))
        return f1, f2
    return pai1.copy(), pai2.copy()

def mutacao(individuo, taxa_mutacao=0.10):
    individuo = individuo.copy()
    N = len(individuo)
    for col in range(N):
        if random.random() < taxa_mutacao:
            individuo[col] = random.randint(1, N)
    return individuo

def algoritmo_genetico(N=8, tam_pop=100, num_geracoes=300, taxa_crossover=0.85, taxa_mutacao=0.10, elitismo=True, verbose=True):
    Populacao = gera_populacao_inicial(N, tam_pop)
    custos = [conta_ataques(ind) for ind in Populacao]
    melhor_custo = min(custos)
    melhor_ind = Populacao[custos.index(melhor_custo)].copy()
    
    hist_melhor = [melhor_custo]
    hist_media = [float(np.mean(custos))]
    
    if melhor_custo == 0:
        if verbose:
            print("[+] Solução encontrada na população inicial!")
        return melhor_ind, 0, 0, hist_melhor, hist_media
        
    for geracao in range(1, num_geracoes + 1):
        nova_populacao = []
        if elitismo:
            indices_ordenados = np.argsort(custos)
            nova_populacao.append(Populacao[indices_ordenados[0]].copy())
            nova_populacao.append(Populacao[indices_ordenados[1]].copy())
            
        while len(nova_populacao) < tam_pop:
            p1 = selecao(Populacao)
            p2 = selecao(Populacao)
            f1, f2 = crossover(p1, p2, taxa_crossover)
            f1 = mutacao(f1, taxa_mutacao)
            f2 = mutacao(f2, taxa_mutacao)
            nova_populacao.append(f1)
            if len(nova_populacao) < tam_pop:
                nova_populacao.append(f2)
                
        Populacao = nova_populacao
        custos = [conta_ataques(ind) for ind in Populacao]
        
        ger_melhor_custo = min(custos)
        ger_melhor_ind = Populacao[custos.index(ger_melhor_custo)]
        
        if ger_melhor_custo < melhor_custo:
            melhor_custo = ger_melhor_custo
            melhor_ind = ger_melhor_ind.copy()
            
        hist_melhor.append(melhor_custo)
        hist_media.append(float(np.mean(custos)))
        
        if verbose and (geracao % 10 == 0 or melhor_custo == 0):
            print(f"Geração {geracao:3d} | Menor Conflito: {melhor_custo:2d} | Média População: {np.mean(custos):.2f}")
            
        if melhor_custo == 0:
            return melhor_ind, melhor_custo, geracao, hist_melhor, hist_media
            
    return melhor_ind, melhor_custo, num_geracoes, hist_melhor, hist_media

def desenha_tabuleiro_ascii(VT):
    N = len(VT)
    print("\n   +---+---+---+---+---+---+---+---+")
    for lin in range(1, N + 1):
        linha_str = f" {lin} |"
        for col in range(N):
            if VT[col] == lin:
                linha_str += " Q |"
            else:
                linha_str += "   |"
        print(linha_str)
        print("   +---+---+---+---+---+---+---+---+")
    print("     A   B   C   D   E   F   G   H\n")

if __name__ == "__main__":
    print("=" * 60)
    print("  RESOLVENDO O PROBLEMA DAS 8 RAINHAS COM ALGORITMO GENÉTICO")
    print("=" * 60)
    
    t0 = time.time()
    solucao, custo, geracao, hist_melhor, hist_media = algoritmo_genetico(verbose=True)
    dt = time.time() - t0
    
    print("\n" + "=" * 60)
    print("  RESULTADO FINAL")
    print("=" * 60)
    print(f"Vetor da Solução (VT) : {solucao}")
    print(f"Número de Ataques     : {custo}")
    print(f"Geração de Resolução  : {geracao}")
    print(f"Tempo de Execução     : {dt:.2f} s")
    print(f"Status                : {'SUCESSO! Solução Ótima sem Conflitos!' if custo == 0 else 'Limite de gerações atingido'}")
    
    print("\nDisposição das Rainhas no Tabuleiro (Q = Rainha):")
    desenha_tabuleiro_ascii(solucao)
