import random
import sys
import main
import math
import random

def inicializa(populacaoAvaliada): #funcao que chamará as outras
    melhorIndividuo(populacaoAvaliada)

def melhorIndividuo(populacaoAvaliada):
    melhorIndividuo = populacaoAvaliada[0]
    return melhorIndividuo

#CLCULA A SOMA DAS AVALIAÇÕES DOS INDIVÍDUOS E RETORNA
def somaAvaliacao(populacaoAvaliada):
    soma = 0
    for i in range(len(populacaoAvaliada)):
        soma += populacaoAvaliada[i][7][0]
    return soma

#CALCULA PROPORÇÃO ROLETA E SALVA NO INDICE [I][8]
def calculaProporcao(populacaoAvaliada):
    pior = populacaoAvaliada[len(populacaoAvaliada)-1][7][0]
    for i in range(len(populacaoAvaliada)):
        valor = int((populacaoAvaliada[i][7][0]/pior) * 100) - 100
        populacaoAvaliada[i][8] = abs(valor)

#SELECIONA O PAI E RETORNA
def selecionaPai(populacaoAvaliada, somaAvaliacao):
    pai = -1
    valorSorteado = random.random() * somaAvaliacao
    soma = 0
    i = 0
    while i < len(populacaoAvaliada) and soma < valorSorteado:
        if populacaoAvaliada[i][8] == 0:
            soma += populacaoAvaliada[i][7][0]  #populacaAvaliada[i][7][0] = custo total do individuo = nota_avaliacao
        else:
            soma += populacaoAvaliada[i][7][0] * (populacaoAvaliada[i][8] / 10) * 2
        pai += 1
        i += 1
    return pai

def mutacao(taxaMutacao, filho, mapa, bits):
    cromossomo = filho

    if random.random() < taxaMutacao:
        if random.random() < 0.5:
            if len(mapa) == 0:
                p1 = random.choice(cromossomo[1])
                pos1 = cromossomo[1].index(p1)
                
            else:
                p1 = random.choice(mapa)
                pos1 = mapa.index(p1)
        else:
            p1 = random.choice(cromossomo[1])
            pos1 = cromossomo[1].index(p1)
        p2 = random.choice(cromossomo[1])
        while p1 == p2:
            p2 = random.choice(cromossomo[1])
        pos2 = cromossomo[1].index(p2)

        cromossomo[1][pos1] = p2
        cromossomo[1][pos2] = p1

    for i in range(len(cromossomo[1])):
        if isinstance(cromossomo[1][i], int):
            cromossomo[1][i] = bin(cromossomo[1][i])[2:]
            auxiliar4 = ''
            if len(cromossomo[1][i]) < bits:
                controlador = len(cromossomo[1][i])
                while controlador < bits:
                    auxiliar4 += '0'
                    controlador += 1
                cromossomo[1][i] = auxiliar4 + cromossomo[1][i]

    
    #print("CROMOSSOMO MUTACAO",cromossomo)
    return cromossomo

def troca(filho, bits):
    cromossomo = filho                  #A variavel filha agora é Cromossomo

    total = pow(2, bits)    
    mapa = list(range(total))           #cria um mapa decimal
    mapaBinario = list(range(total))    #Cria outro mapa decimal

    #Converte o mapa decimal em binario-------------------------------
    for i in range(len(mapaBinario)):
        mapaBinario[i] = bin(mapaBinario[i])[2:]
        auxiliarConverter = ''
        if  len(mapaBinario[i]) < bits:
            controlador = len(mapaBinario[i])
            while controlador < bits:
                auxiliarConverter += '0'
                controlador += 1
            mapaBinario[i] = auxiliarConverter + mapaBinario[i]
    #------------------------------------------------------------------

    for i in range(len(cromossomo[1])):
        if cromossomo[1][i] in mapaBinario:
            mapaBinario.remove(cromossomo[1][i])

    #print(mapaBinario)
    if not len(mapaBinario) == 0:
        for j in range(len(cromossomo[1])):
            for k in range(j+1, len(cromossomo[1])):
                if cromossomo[1][j] == cromossomo[1][k]:
                    valor = random.choice(mapaBinario)
                    mapaBinario.append(cromossomo[1][j])
                    cromossomo[1][j] = valor
                        
                    mapaBinario.remove(valor)
                if j+1 > len(cromossomo[1]):
                    break

    #print("CROMOSSOMO SAIDA TROCA",cromossomo, "\n")
    return cromossomo

def crossover(individuo1, individuo2):
    cromossomo1 = individuo1[2]
    cromossomo2 = individuo2[2]
    corte = round(random.random() * len(individuo1[2]))
    
    filho1 = []
    aux = individuo1[2][0][0::]
    filho1.append(aux)
    filho1.append(individuo2[2][1][0:corte] + individuo2[2][1][corte::])
    filho1.append(individuo1[9])


    filho2 = []
    aux = individuo1[2][0][0::]
    filho2.append(aux)
    filho2.append(individuo1[2][1][0:corte] + individuo2[2][1][corte::])
    filho2.append(individuo2[9])

    filhos = []
    filhos.append(filho1)
    filhos.append(filho2)

    return filhos







