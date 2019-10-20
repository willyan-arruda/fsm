import main
import math
import random
import time
import os



#lê arquivo da FSM
arq = open('kiss2/bbtas.kiss2', 'r')
print("FSM em execução:", )

#Cria lista com as linhas
lista = arq.readlines()

#Lê a quantidade de estados da FSM
quantidadeEstados = int(lista[4].split()[1])

#Lê a quantidade de bits de entrada da FSM
bitin = int(lista[1].split()[1])
print("Quantidade de bits de entrada: ", bitin)

#Lê a quantidade de bits de saída da FSM
bitout = int(lista[2].split()[1])
print("Quantidade de bits de saida", bitout)

#Le o tamanho da FSM
tamFSM = int(lista[3].split()[1])
print("Tamanho da FSM: ", tamFSM)

#Calcula a quantidade de bits necessários para a FSM, 
#aplica log da quantidade de Estados na base 2 e com math.ceil
#arredonda para o próximo teto
bits = math.ceil(math.log2(quantidadeEstados))
print("Quantidade de bits: ", bits)

#Cria uma lista de entradas da FSM
entradas = []

#Preenche a lista criada com as possíveis entradas para a FSM lida
for i in range(2 ** bitin):
    entradas.append(format(i,'0'+str(bitin)+'b'))

#Calcula o tamanho da população a ser gerada
tamanhoPopulacao = 2*quantidadeEstados*bits
quantGeracoes = math.ceil(tamFSM ** 0.5) ** bits
tamanhoIndividuo = pow(2, bits)

print("Quantidade de gerações calculadas para a FSM: ", quantGeracoes)

#Define a taxa de mutação
taxaMutacao = 0.02

#Define a taxa de cruzamento
taxaCruzamento = int(0.4 * tamanhoPopulacao)

#Lê a hora inicial
inicio = time.time()


print(main.inicializa(tamanhoIndividuo, quantGeracoes, tamanhoPopulacao, taxaMutacao, entradas, bits, bitin, bitout, tamFSM, quantidadeEstados, lista, taxaCruzamento)[0])

#Lê a hora final
fim = time.time()

#Calcula o tempo de execução
temp = fim - inicio
print("Tempo de execução: ", temp)
