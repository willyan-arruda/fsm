import math
import random
import multiprocessing #(Uitilizado para obter a quant. de Threads do PC)
import _thread #(metodo 1 de paralelização)
import threading #(metodo 2 de paralelização)
import string
import time
import sys
import algoritmoGenetico
from operator import itemgetter
from sympy.logic import SOPform
from sympy import symbols

populacao = []
populacaoAvaliada = []
listaMelhoresSolucoes = []
controleThread = [] #Utilizado somente no primeiro método de paralização

#Função que chamará as outras
def inicializa(tamanhoIndividuo, quantGeracoes, tamanhoPopulacao, taxaMutacao, entradas, bits, bitin, bitout, tamFSM, quantidadeEstados, lista, taxaCruzamento): 
	
	for x in range(quantGeracoes):
		#cria lista com as melhores solucoes
		for i in range(len(populacao), tamanhoPopulacao):
			#gera tabela com base na FSM lida
			tabela = geraTabela(lista)
			#Cria mapa do individuo
			mapaIndividuo =  geraMapaIndiviuo(tamanhoIndividuo, bits)
			#Gera Cromossomo
			cromossomo = geraCromossomo(mapaIndividuo, tabela, quantidadeEstados, lista, bits)
			#Preenche tabela com o cromossomo gerado
			preencheTabela(tabela, lista, cromossomo, quantidadeEstados, bits)
			#Cria Variáveis de Próx Estado
			variaveisProxEstado = criarVariaveis(bits, 'y')
			#Cria Variaveis de saída
			variaveisSaida = criarVariaveis(bitout, 's')
			#Gera colunas de saída com mintermos
			mintermos = criaColunas(bitin, bits, entradas, tabela, cromossomo, variaveisProxEstado, 4, 'y')
			#Gera colunas com mintermos da saída
			mintermosSaida = criaColunas(bitin, bits, entradas, tabela, cromossomo, variaveisSaida, 5, 's')
			#Obtem os dontcares
			dontcares = obterDontcare(entradas, bits, cromossomo, mapaIndividuo)
			#Cria Variaveis do indivíduo
			individuo = variaveisIndividuo(tabela, mintermos, cromossomo, dontcares, mintermosSaida, mapaIndividuo)
			#Adiciona o individuo na populacao
			populacao.append(individuo)
		
		#chama a função que calcula 
		calculaCustoParalelo(bitin, bits, entradas)
		#ordena a populacao utilizando o quick sort
		ordenaPopulacao(populacaoAvaliada)
		#Obtem o melhor individuo da populacao
		melhorIndiviuo = algoritmoGenetico.melhorIndividuo(populacaoAvaliada)
		#Calcula proporção de cada individuo
		algoritmoGenetico.calculaProporcao(populacaoAvaliada)
		#Adiciona o melhor individuo na lista de melhores solucoes
		listaMelhoresSolucoes.append(melhorIndiviuo)
		#Realiza a soma das avaliações dos indivíduos da populacao
		somaAvaliacoesIndividuos = algoritmoGenetico.somaAvaliacao(populacaoAvaliada)
		#cria lista de nova populacao
		novaPopulacao = []

		print("<<--------------------------------------------------------------------------------------------------------->>")
		print("Melhor indivíduo da geração ", x)
		print(melhorIndiviuo[2], "Custo: ", melhorIndiviuo[7][0])
		print("Expressão: ", melhorIndiviuo[6][2])
		print("<<==========================================================================================================>>")

		for individuosGerados in range(0, taxaCruzamento, 2):

			pai1 = algoritmoGenetico.selecionaPai(populacaoAvaliada, somaAvaliacoesIndividuos)
			pai2 = algoritmoGenetico.selecionaPai(populacaoAvaliada, somaAvaliacoesIndividuos)

			if pai1 == pai2:
				pai2 = algoritmoGenetico.selecionaPai(populacaoAvaliada, somaAvaliacoesIndividuos)
			
			filhos = []
			filhos = algoritmoGenetico.crossover(populacaoAvaliada[pai1], populacaoAvaliada[pai2])

			for i in range(len(filhos)):
				if len(filhos[i][1]) == len(set(filhos[i][1])):
					novaPopulacao.append(algoritmoGenetico.mutacao(taxaMutacao, filhos[i], filhos[i][2], bits))
				else:
					novaPopulacao.append(algoritmoGenetico.troca(filhos[i], bits))
		
		preparaNovaGeracao(novaPopulacao, lista, quantidadeEstados, bits, bitout, bitin, entradas, tamanhoIndividuo)
	
	ordenaPopulacao(listaMelhoresSolucoes)

	return listaMelhoresSolucoes
		

def preparaNovaGeracao(novaPopulacao, lista, quantidadeEstados, bits, bitout, bitin, entradas, tamanhoIndividuo):
	#populacao.clear()
	populacaoAvaliada.clear()

	populacaoTemp = [] #Cria um vetor de populacao temporaria

	for i in range(len(novaPopulacao)):
		#Pega o mapa do individuo gravado no indice 2
		mapaIndividuo =  novaPopulacao[i][2]
		#Gera uma tabela com base na lista
		tabela = geraTabela(lista)
		#A variavel cromossomo assume um individuo da populacao
		cromossomo = novaPopulacao[i]
		#Preenche tabela com o cromossomo gerado
		preencheTabela(tabela, lista, cromossomo, quantidadeEstados, bits)
		#Cria Variáveis de Próx Estado
		variaveisProxEstado = criarVariaveis(bits, 'y')
		#Cria Variaveis de saída
		variaveisSaida = criarVariaveis(bitout, 's')
		#Gera colunas de saída com mintermos
		mintermos = criaColunas(bitin, bits, entradas, tabela, cromossomo, variaveisProxEstado, 4, 'y')
		#Gera colunas com mintermos da saída
		mintermosSaida = criaColunas(bitin, bits, entradas, tabela, cromossomo, variaveisSaida, 5, 's')
		#Obtem os dontcares
		dontcares = obterDontcare(entradas, bits, cromossomo, mapaIndividuo)
		#Cria Variaveis do indivíduo
		individuo = variaveisIndividuo(tabela, mintermos, cromossomo, dontcares, mintermosSaida, mapaIndividuo)
		#Adiciona o individuo na populacao
		populacaoTemp.append(individuo)

	#Remove aleatoriamente individuos da populacao antiga
	for i in range(len(populacaoTemp)):
		aux = random.choice(populacao)
		populacao.remove(aux)

	populacaoTemp2 = populacao
	populacao.clear()
	populacao.extend(populacaoTemp)
	calculaCustoParalelo(bitin, bits, entradas)
	populacao.extend(populacaoTemp2)

	ordenaPopulacao(populacao)
	listaMelhoresSolucoes.append(populacao[0])

#-----------------------------------------------


#Gera mapa de seleção aleatória para o individuo-------------------
def geraMapaIndiviuo(tamanhoIndividuo, bits):
	mapaIndividuo = list(range(tamanhoIndividuo))

	#Converte o mapa em binário-------------------------------------
	for i in range(len(mapaIndividuo)):
		mapaIndividuo[i] = bin(mapaIndividuo[i])[2:]
		auxiliarConverter = ''
		if len(mapaIndividuo[i]) < bits:
			controlador = len(mapaIndividuo[i])
			while controlador < bits:
				auxiliarConverter += '0'
				controlador += 1
			mapaIndividuo[i] = auxiliarConverter + mapaIndividuo[i]
	#-----------------------------------------------------------------
	return mapaIndividuo
#--------------------------------------------------------------------

#Cria tabela com os estados da FSM lida e suas entradas
def geraTabela(lista):
	tabela = []
	quantLinhas = len(lista)
	
	for i in range(5, quantLinhas):
		auxiliar = lista[i].split()
		listaTemp = []
		contador = 0

		for j in range(6):
			if j == 2 or j == 4:
				listaTemp.append('')
			else:
				if '-' in auxiliar[contador]:
					auxiliar[contador] = auxiliar[contador].replace('-', '0')
				listaTemp.append(auxiliar[contador])
				contador += 1
		tabela.append(listaTemp)
	return tabela
#--------------------------------------------------------
		
def geraCromossomo(mapaIndividuo, tabela, quantidadeEstados, lista, bits):
	quantLinhas = len(tabela)
	cromossomo = []

	#Gera o cromossomo com base na FSM lida
	auxiliar = []
	for i in range(quantLinhas):
		if tabela[i][1] not in auxiliar:
			auxiliar.append(tabela[i][1])
		if tabela[i][3] not in auxiliar:
			auxiliar.append(tabela[i][3])
	cromossomo.append(auxiliar)
	#---------------------------------------
	
	#Preenche o conteúdo do cromossomo com o mapa gerado
	auxiliar2 = []
	for j in range(quantidadeEstados):
		conteudo = random.choice(mapaIndividuo)
		auxiliar2.append(conteudo)
		mapaIndividuo.remove(conteudo)
	cromossomo.append(auxiliar2)
	#----------------------------------------------------

	#Na posição [0] está os passos da FSM
	#Na posição [1] está o cromossomo gerado
	return cromossomo
#--------------------------------------------------------

#Preenche a tabela criada com base no cromossomo gerado
def preencheTabela(tabela, lista, cromossomo, quantidadeEstados, bits):
	#print("Tabela antiga \n", tabela)
	quantLinhas = len(lista)

	for i in range(quantLinhas - 5):
		for j in range(2, 5, 2):
			for k in range(quantidadeEstados):
				#Escreve na tabela
				if tabela[i][j-1] == cromossomo[0][k]:
					tabela[i][j] = cromossomo[1][k]
#----------------------------------------------------------

#Cria variáveis do individuo
def variaveisIndividuo(tabela, mintermos, cromossomo, dontcares, mintermosOut, mapaIndividuo):
	individuo = []
	avaliacao = []
	avaliacaoSaida = []
	total = []
	proporcaoRoleta = []

	individuo.append(tabela)
	individuo.append(mintermos)
	individuo.append(cromossomo)
	individuo.append(dontcares)
	individuo.append(avaliacao)
	individuo.append(mintermosOut)
	individuo.append(avaliacaoSaida)
	individuo.append(total)
	individuo.append(proporcaoRoleta)
	individuo.append(mapaIndividuo)

	return individuo

#Cria variáveis de próximo estado----------------
def criarVariaveis(bits, variavel):
	listaVariaveis = {}
	mintermos = {}
	saida = []
	for i in range(bits):
		l = []
		listaVariaveis[variavel + str(i)] = l
		mintermos[variavel + str(i)] = l
	
	saida.append(listaVariaveis)
	saida.append(mintermos)

	#print(saida)
	return saida
#--------------------------------------------------

def criaColunas(bitin, bits, entradas, tabela, cromossomo, variaveisProxEstado, indice, variavel):
	listaVariaveis = variaveisProxEstado[0]

	for item in tabela:
		for j in range(len(listaVariaveis)):
			listaVariaveis[variavel+str(j)].append(item[indice][j])
		
	mintermos = variaveisProxEstado[1] #Obtém os mintermos de cada variável

	for i in range(len(mintermos)):
		mintermos[variavel + str(i)] = obterMintermos(listaVariaveis[variavel + str(i)], tabela)
	

	return mintermos
		
def obterMintermos(listaVariaveis, tabela):
	auxiliar = []
	mintermos = []
	contador = 0

	for valor in listaVariaveis:
		if valor == '1':
			auxiliar.append(tabela[contador][0] + tabela[contador][2])
		
		contador+= 1

	for i in auxiliar:
		novo = []
		for x in range(len(i)):
			novo.append(int(i[x]))
		mintermos.append(novo)
	
	return mintermos

def obterDontcare(entradas, bits, cromossomo, mapaIndividuo):	
	for i in range(len(cromossomo[1])):
		if cromossomo[1][i] in mapaIndividuo:
			mapaIndividuo.remove(cromossomo[1][i])

	no_used = []

	"""for x in mapaIndividuo:
		aux = converter(x, bits)
		no_used.append(aux)"""

	dontcare = []
	for i in entradas:
		for j in no_used:
			dontcare.append(i + j)

	teste = []
	for i in dontcare:
		aux = []
		for x in range(len(i)):
			aux.append(int(i[x]))
		teste.append(aux)

	return teste

def converter(num, bits):
	binario = bin(num)[2:]
	aux = ''
	if len(binario) < bits:
		t = len(binario)
		while t < bits:
			aux += '0'
			t += 1
		binario = aux + binario

	return binario

def retornaCusto(populacaoCortada, bitin, bits, entradas):
	for i in range(len(populacaoCortada)):
		mintermos = populacaoCortada[i][1]
		cromossomo = populacaoCortada[i][2]
		dontcares = populacaoCortada[i][3]
		mintermosOut = populacaoCortada[i][5]

		n = bits + bitin
		var = list(string.ascii_lowercase[:n])
		test = symbols(var)

		#CALCULA CUSTOS DOS MINTERMOS DE SAIDA--------------
		auxiliarCont = []
		auxiliarTermos = []
		auxiliarExpressao = []
		avaliacao = []

		
		for j in range(len(mintermos)):
			resultado = SOPform(test, mintermos['y' + str(j)], dontcares)    
			expressao = str(resultado)
			termos = expressao.count('|')+1
			cont = 0
			for l in expressao:
				if l in var:
					cont +=1
			
			cont += termos
		
			auxiliarCont.append(cont)
			auxiliarTermos.append(termos)
			auxiliarExpressao.append(expressao)
		avaliacao.append(auxiliarCont)
		avaliacao.append(auxiliarTermos)
		avaliacao.append(auxiliarExpressao)

		populacaoCortada[i][4] = avaliacao

		#CALCULA CUSTO DAS SAIDAS DA FSM---------------------------
		auxiliar2Cont = []
		auxiliar2Termos = []
		auxiliar2Expressao = []
		avaliacaoOut = []
		for m in range(len(mintermosOut)):
			resultado = SOPform(test, mintermosOut['s' + str(m)], dontcares)
			expressao = str(resultado)
			termos = expressao.count('|')+1
			cont = 0
			for n in expressao:
				if n in var:
					cont +=1
			cont += termos
		
			auxiliar2Cont.append(cont)
			auxiliar2Termos.append(termos)
			auxiliar2Expressao.append(expressao)
		avaliacaoOut.append(auxiliar2Cont)
		avaliacaoOut.append(auxiliar2Termos)
		avaliacaoOut.append(auxiliar2Expressao)
		populacaoCortada[i][6] = avaliacaoOut


		custoTotal = 0
		tempCusto = populacaoCortada[i][4][0] #pega o custo do individuo
		for x in range(len(populacaoCortada[i][6][0])): #for com repetições do tamanho do custo de saida
			tempCusto.append(populacaoCortada[i][6][0][x])
		custoTotal = sum(tempCusto)

		termosTotal = 0
		tempTermos = populacaoCortada[i][4][1] #pega os termos do individuo
		for y in range(len(populacaoCortada[i][6][1])):
			tempTermos.append(populacaoCortada[i][6][1][y])
		custoTermos = sum(tempTermos)

		aux = []
		aux.append(custoTotal)
		aux.append(custoTermos)
		populacaoCortada[i][7] = aux

		populacaoAvaliada.append(populacaoCortada[i])

	#Pelo método 1 de paralização, quando a Thread termina ela sai silenciosamente e retorna. Dessa forma conforme as Threads forem terminando
	#o Array controleThread é escrito com um valor qualquer, apenas para controle
	return controleThread.append("1")

def calculaCustoParalelo(bitin, bits, entradas):

	#print("numeros de cpu: ", multiprocessing.cpu_count())
	quantNucleos = multiprocessing.cpu_count()

	#Divide array de populacao pela quantidade de nucleos da maquina
	populacaoCortada = []
	tamanhoPopulacao = len(populacao)
	for i in range(quantNucleos):
		start = int(i*tamanhoPopulacao/quantNucleos)
		end = int((i+1)*tamanhoPopulacao/quantNucleos)
		populacaoCortada.append(populacao[start:end])
	

	#Metodo 1 de paralelização-------------------------------------------------------------
	for j in range(len(populacaoCortada)):
		#Cria J Threads e entrega cada fatia para calculo a cada uma
		_thread.start_new_thread(retornaCusto, (populacaoCortada[j], bitin, bits, entradas,))

	#Este While ficará esperando as Threads retornarem
	#Enquanto o tamanho do array controleThread não for diferente da quant. de nucleos que é = a quant. de fatias, o código fica esperando
	while len(controleThread) != quantNucleos :
		pass
	#Quando as Threads retornam, limpa o array de controle e continua o código.
	controleThread.clear()
	#--------------------------------------------------------------------------------------"""

	#Sem paralelismo----------------------------------
	#retornaCusto(populacao, bitin, bits, entradas)

	"""#Metodo 2 de paralelização------------------------------------------------------------
	for j in range(len(populacaoCortada)):
		variavel = threading.Thread(target=retornaCusto,args=(populacaoCortada[j], bitin, bits, entradas))
		variavel.start()

	#verifica se outros processos encerraram
	while (len(threading.enumerate()) > 1):
		pass
	#----------------------------------------------------------------------------------------"""

def partition(arr, low, high):
	i = (low-1)
	pivot = arr[high][7][0]

	for j in range(low, high):
		if arr[j][7][0] <= pivot:
			i = i+1
			arr[i], arr[j] = arr[j],arr[i]
	
	arr[i+1],arr[high] = arr[high],arr[i+1]
	return(i+1)

def quickSort(arr, low, high):
	if low < high:
		pi = partition(arr,low,high)
		quickSort(arr, low, pi-1)
		quickSort(arr, pi+1, high)


def ordenaPopulacao(populacaoAvaliada):
	arr = populacaoAvaliada
	n = len(arr)
	quickSort(arr,0,n-1)
	populacaoAvaliada = arr







