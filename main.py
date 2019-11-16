import re, random, time

# Essa lista irá armazenar a ordem que a posição da memória
# principal foi inserida na memória cache, quando ocorre um CACHE MISS
# a posição ZERO dessa lista será removida e a nova posição de memória
# será inserida no topo da lista.
contador_fifo = {}

def tempoExecucao(segundos_total):
    dias = segundos_total // 86400
    segrest1 = segundos_total % 86400

    hora = segrest1 // 3600
    segrest2 = segrest1 % 3600

    minutos = segrest2 // 60
    segundos_finais = segrest2 % 60
    print("Tempo de execução:",dias, "dias,", hora, "horas,", minutos, "minutos e", round(segundos_finais,3), "segundos.")

def verifica_posicao_vazia(memoria_cache, qtdConjuntos, posicao_memoria):
    #Verifica se existe na cache uma posição de memória que ainda não foi utilizada,
    #se existir, essa posição é retornada

  numConjunto = get_ncpm(posicao_memoria, qtdConjuntos)
  lista_posicoes = get_lista_posicoes(memoria_cache, numConjunto, qtdConjuntos)

  for x in lista_posicoes: #verifica se alguma posicção do conjunto está vazia
    if memoria_cache[x] == -1:
      return x
  return -1

def inicia_contador_fifo():
  """Seta os valores do contador fifo para que a primeira subsitituição
  ocorra no primeiro elemento que faz parte do conjunto
  """
  # cria no contador fifo uma posição para cada conjunto
  for i in range(0,qtdConjuntos):
      contador_fifo[i]=0

def get_ncpm(posicao_memoria, qtdConjunto): #retorna o valor inteiro do resto da divisao dos atributos
    return int(posicao_memoria)%int(qtdConjuntos)

def imprimeCd(cache):
  print("\n---------------------------")
  print("|      Cache Direto        |")
  print("---------------------------")
  print("|Tamanho Cache: {:>11}| ".format(len(cache)))
  print("---------------------------")
  print("|Pos Cache | Posição Memória")
  for posicao, valor in cache.items():
    print("|{:>10}|{:>15}".format(posicao, valor))
  print("\n")

def imprimeCa(cache):

  print("\n")
  print("----------------------------")
  print("|Tamanho Cache: {:>11}| ".format(len(cache)))
  print("|     Cache Associativo    |")
  print("----------------------------")
  print("|Pos Cache | Posição Memória")
  print("----------------------------")
  for posicao, valor in cache.items():
    print("|{:>10}|{:>15}".format(posicao, valor))
  print("\n")

def imprimeAC (cache, qtdConjuntos):
    print("\n")
    print("|Tamanho: {:>21} | \n|Conjuntos: {:>19} |".format(len(cache), qtdConjuntos))
    print("----------------------------")
    print("  Cache Associativo Conjunto  ")
    print("|#PC|  Cnj | Pos memória")
    for posicao, valor in cache.items():
        numConjunto = get_ncpm(posicao, qtdConjuntos)
        print("|{} \t|{:4}\t|  {:>4}".format(posicao, numConjunto, valor))
    print("\n")

def inicializar_cache(totalCache): #cria uma cache zerada utilizando como dicionario (chave, valor) usando como valor padrão -1
    memoria_cache = {} #zera a memória cache
    for x in range(0, totalCache):#para X de 0 até o tamanho total de palavras da cache
        memoria_cache [x] = -1 #isso indica que a posição n foi usada

    return memoria_cache

def verifica_posicao_CA_AC(memoria_cache, qtdConjuntos, posicao_memoria): #verifica se a posição está no modo associativo ou A por conjunto
    numConjunto = int(posicao_memoria)%int(qtdConjuntos)
    while numConjunto < len(memoria_cache): #len() retorna um número de itens no objeto
        if memoria_cache[numConjunto] == posicao_memoria:
            return numConjunto
        numConjunto +=qtdConjuntos
    return -1 #não encontrou posição na memoria

def get_lista_posicoes(memoria_cache, numConjunto, qtdConjuntos):
    # retorna uma lista com todas as posições da memoria que fazem parte de um conjunto

    lista_posicoes = [] #Criar lista de posiçoes
    posicao_inicial = numConjunto
    while posicao_inicial < len(memoria_cache):
        lista_posicoes.append(posicao_inicial) #append adiciona 1 unico item a lista existente
        posicao_inicial +=qtdConjuntos
    #print(lista_posicoes)
    return lista_posicoes

def substituicao_RANDOM(memoria_cache, qtdConjuntos, posicao_memoria):
    # as posições que serão subistituidas serão definidas  de maneira aleátoria

    numConjunto = int(posicao_memoria)%int(qtdConjuntos)

    lista_posicoes = get_lista_posicoes(memoria_cache,numConjunto, qtdConjuntos)

    local_trocar = random.choice(lista_posicoes) #posição da memória cache a ser trocada, selecionada de forma aleatória

    memoria_cache[local_trocar] = posicao_memoria #posição da memória cache selecionada recebe o "valor" da memória principal

def substituicao_FIFO(memoria_cache, qtdConjuntos, posicao_memoria):
    # essa substituição sera feita como uma fila, onde o primeiro elemneto que entrea é o primeiro que sai

    numConjunto = int(posicao_memoria)%int(qtdConjuntos)
    local_trocar = contador_fifo[numConjunto] #define que posição da memória cache será substituida
    lista_posicoes = get_lista_posicoes(memoria_cache,numConjunto, qtdConjuntos)

    # posição da memória cache selecionada recebe o "valor" da memória principal
    memoria_cache[lista_posicoes[local_trocar]] = posicao_memoria
    contador_fifo[numConjunto] += 1
    #print((contador_fifo))

    if contador_fifo[numConjunto] >= (len(memoria_cache)/qtdConjuntos):
        contador_fifo[numConjunto] = 0

def executar_mapeamento_direto(totalCache, posicoesMemoriaAcessar, politica_escrita):
  """Executa a operação de mapeamento direto.

  Argumentos necessarios
    totalCache {int} -- tamanho total de palavras da cache
    posicoesMemoriaAcessar {list} - quais são as posições de memória que devem ser acessadas
  """
  # zera tota a memória cache
  memoria_cache = inicializar_cache(totalCache) #Inicio de uma nova memoria cache

  #print('Situação Inicial da Memória Cache')
  #imprimeCd(memoria_cache)

  hitoumiss = ''
  hit = 0; #Numero inicial de hits/Acertos
  miss = 0 #Numero inicial de miss/Erros
  memoria_principal=0 #numero inicial de escritas na memoria

  for index, posicao_memoria in enumerate(posicoesMemoriaAcessar):
    # no mapeamento direto, cada posição da memória principal tem uma, e apenas uma, posição
    # específica na memória cache, essa posição será calculada em função
    # do mod da posição acessada em relação ao tamanho total da cache
    #i = j módulo m
    #i = número da linha da cache
    #j = número do bloco da memória principal
    #m = número de linhas da cache
    posicao_cache = posicao_memoria % totalCache

    # se a posição de memória principal armazenada na linha da cache for a posição
    # desejada então temos um acerto de cache, caso contrário da miss
    if memoria_cache[posicao_cache] == posicao_memoria:
      hit += 1
      hitoumiss = 'Hit'

    else:
      miss += 1
      hitoumiss = 'Miss'

    if(politica_escrita==1):
        memoria_principal+=1
    elif(politica_escrita==2):
        if(memoria_cache[posicao_cache]!=posicao_memoria):
            memoria_principal+=1


    #Apos a verificaçção, a posição na memoria é atualizada
    #permanece a mesma em caso de acerto
    #Muda em caso de erro e atualiza para a memoria inicialmente desejada
    memoria_cache[posicao_cache] = posicao_memoria

    #print('\nLeitura linha {},  posição de memória desejada {}.'.format(index,posicao_memoria))
    #print('Status: {}'.format(hitoumiss))
    #imprimeCd(memoria_cache)

  print('\n\n------------------------')
  print('   Mapeamento Direto')
  print('------------------------')
  print("Politica de escrita:{}".format(politica_escrita))
  print("Total de escritas na memoria principal: {}".format(memoria_principal))
  print('Total de memórias acessadas: {}'.format(len(posicoesMemoriaAcessar)))
  print('Total HIT: {}'.format(hit))
  print('Total MISS: {}'.format(miss))
  taxaCacheHit = (hit / len(posicoesMemoriaAcessar))*100
  print('Taxa de Cache HIT: {number:.{digits}f}%'.format(number=taxaCacheHit, digits=2))

def executar_mapeamento_associativo(totalCache, posicoesMemoriaAcessar, politicaSubstituicao, politica_escrita):
  #O mapeamento associativo é um caso particular de mapeamento associativo por conjunto

  """Arguments:
    totalCache {int} -- tamanho total de palavras da cache
    posicoesMemoriaAcessar {list} - quais são as posições de memória que devem ser acessadas
    politicaSubstituicao {str} -- RANDOM/ FIFO
  """
  # o número 1 indica que haverá apenas um único conjunto no modo associativo por conjunto
  # que é igual ao modo associativo padrão!

  executar_mapeamento_associativo_conjunto(totalCache, 1, posicoesMemoriaAcessar, politicaSubstituicao,politica_escrita)

def executar_mapeamento_associativo_conjunto(totalCache, qtdConjuntos, posicoesMemoriaAcessar,politicaSubstituicao, politica_escrita):
    """Executa a operação de mapeamento associativo, ou seja, não existe uma posição específica
    para o mapemento de uma posição de memória.

    Arguments:
      totalCache {int} -- tamanho total de palavras da cache
      qtdConjuntos {int} -- quantidade de conjuntos na cache
      posicoesMemoriaAcessar {list} -- quais são as posições de memória que devem ser acessadas
      politicaSubstituicao {str} -- RANDOM
    """
    memoria_cache = inicializar_cache(totalCache)  # Inicia nova memoria cache

    # se o número de conjuntos for igual a zero, então a simulação é feita
    # com cache associativo
    nome_mapeamento="Associativo"
    #if qtdConjuntos == 1:
        #imprimeCa(memoria_cache)
    if qtdConjuntos!=1:
        nome_mapeamento="Associativo por conjunto"
        #imprimeAC(memoria_cache, qtdConjuntos)

    hit = 0
    miss = 0
    memoria_principal=0

    # se a política for fifo então inicializa a lista de controle
    if politicaSubstituicao == 'FIFO':
        inicia_contador_fifo()

    # percorre cada uma das posições de memória que estavam no arquivo
    for index, posicao_memoria in enumerate(posicoesMemoriaAcessar):
        #print('\n\n\nInteração número: {}'.format(index + 1))
        # verificar se existe ou não a posição de memória desejada na cache
        inserirMemoriaPosicaoCache = verifica_posicao_CA_AC(memoria_cache, qtdConjuntos,
                                                                             posicao_memoria)

        # a posição desejada já está na memória
        if inserirMemoriaPosicaoCache >= 0:
            hit += 1
            #print('Cache HIT: posiçao de memória {}, posição cache {}'.format(posicao_memoria,inserirMemoriaPosicaoCache))
        else:
            miss += 1
            #print('Cache MISS: posiçao de memória {}'.format(posicao_memoria))

            # verifica se existe uma posição vazia na cache, se sim aloca nela a posição de memória
            posicao_vazia=verifica_posicao_vazia(memoria_cache, qtdConjuntos, posicao_memoria)

            # se posicao_vazia for < 0 então devemos executar as políticas de substituição

            if posicao_vazia >= 0:
                memoria_cache[posicao_vazia] = posicao_memoria
            elif politicaSubstituicao == 'RANDOM':
                substituicao_RANDOM(memoria_cache, qtdConjuntos, posicao_memoria)
            elif politicaSubstituicao == 'FIFO':
                substituicao_FIFO(memoria_cache, qtdConjuntos, posicao_memoria)

        if (politica_escrita == 1):
            memoria_principal += 1
        elif (politica_escrita == 2):
            if (inserirMemoriaPosicaoCache<0):
                memoria_principal += 1
        #if qtdConjuntos == 1:
            #imprimeCa(memoria_cache)
            #print(posicao_memoria)
            #print(contador_fifo)
            #print(qtdConjuntos)
        #else:
            #imprimeAC(memoria_cache, qtdConjuntos)
            #print(posicao_memoria)
            #print(contador_fifo)
            #print(qtdConjuntos)

    print('\n\n-----------------')
    print('Resumo Mapeamento {}'.format(nome_mapeamento))
    print('-----------------')
    print('Política de Substituição: {}'.format(politicaSubstituicao))
    print('-----------------')
    print("Politica de escrita:{}".format(politica_escrita))
    print("Total de escritas na memoria principal: {}".format(memoria_principal))
    print('Total de memórias acessadas: {}'.format(len(posicoesMemoriaAcessar)))
    print('Total HIT {}'.format(hit))
    print('Total MISS {}'.format(miss))
    taxaCacheHit = (hit / len(posicoesMemoriaAcessar)) * 100
    print('Taxa de Cache HIT {number:.{digits}f}%'.format(number=taxaCacheHit, digits=2))

def alunos():
    print("Alunos: Marcos Antonio")
    print("        Mercia costa")
    print("        David Barboza")
    print("        Caylon Solon")
    print("        Flavio Sena")

##Função main que controlará toda a execução do processo##
totalCache = int(input("Defina o numero de posições da memoria cache:"))
tipo =int(input("Tipo de mapeamento\n1-Direto   2-Associativo   3-Associativo conjunto\n"))
politica_escrita=int(input("Politica de escrita\n1-Write-throught   2-Write-back"))

if(tipo==2):
    politica= int(input("Politica de substituição\n1-RANDOM 2-FIFO 3-AMBAS\n "))
    if(politica==1):
        politicaSubstituicao='RANDOM'
    elif(politica==2):
        politicaSubstituicao='FIFO'
    else:
        politicaSubstituicao='AMBAS'
    #politicaSubstituicao.upper()
    qtdConjuntos=1
elif(tipo==3):
    politica=int(input("Politica de substituição\n1-RANDOM 2-FIFO 3-AMBAS\n"))
    if (politica == 1):
        politicaSubstituicao = 'RANDOM'
    elif (politica == 2):
        politicaSubstituicao = 'FIFO'
        #print(politicaSubstituicao)
    elif(politica==3):
        politicaSubstituicao = 'AMBAS'
    #politicaSubstituicao.upper()
    qtdConjuntos = int(input("Quantidade de conjuntos:"))

arquivoAcesso = input("Arquivo de acesso:")

#Tratamento de pequenas excessoes

if arquivoAcesso == "":
  print('\n\n------------------------------')
  print('É necesário informar o nome do arquivo que será processado')
  print('------------------------------')
  exit()

# lê o arquivo e armazena cada uma das posições de memória que será lida em uma lista/vetor
try:
    f = open(arquivoAcesso, "r")

    posicao_memoria = f.readlines()
    posicoesMemoriaAcessar = []
    for linha in posicao_memoria:
        posicoesMemoriaAcessar.append(int(linha.strip()[2:10],16))
        #print(linha.strip()[2:10])
    #print(posicoesMemoriaAcessar)
    """posicoesMemoriaAcessar = []
    for posicaoMemoria in f:
        posicoesMemoriaAcessar.append(int(re.sub(r"\r?\n?$", "", posicaoMemoria, 1),16))
    for i in range(0,len(posicoesMemoriaAcessar)):
        print(posicoesMemoriaAcessar[i])"""
    f.close()

except IOError as identifier:
  print('\n\n------------------------------')
  print('Arquivo \'{}\'não encontrado.'.format(arquivoAcesso))
  print('------------------------------')
  exit()

#Caso o numero de posiçoes seja igual a zero
if len(posicoesMemoriaAcessar) == 0:
    print('\n\n------------------------------')
    print('arquivo {} impossivel de ser lido'.format(arquivoAcesso))
    print('------------------------------')
    exit()

print('====================================')
print('| SIMULADOR DE MEMORIA CACHE CACHE |')
alunos()
print('====================================')
time.sleep(1)

inicio=time.time()
#Mapeamento Direto
if tipo == 1:
  executar_mapeamento_direto(totalCache, posicoesMemoriaAcessar, politica_escrita)
  fim=time.time()
  segundos_total=fim-inicio
  print(tempoExecucao(segundos_total))

#Mapeamento associativo
elif tipo ==2:
  if (politicaSubstituicao =='AMBAS'):
    executar_mapeamento_associativo(totalCache, posicoesMemoriaAcessar, 'RANDOM', politica_escrita)
    executar_mapeamento_associativo(totalCache, posicoesMemoriaAcessar, 'FIFO', politica_escrita)
    fim=time.time()
    segundos_total = fim - inicio
    print(tempoExecucao(segundos_total))
  else:
    executar_mapeamento_associativo(totalCache, posicoesMemoriaAcessar, politicaSubstituicao,politica_escrita)
    fim=time.time()
    segundos_total = fim - inicio
    print(tempoExecucao(segundos_total))

#Mapeamento Associativo Conjunto
elif tipo == 3:
  # o número de conjuntos deve ser um divisor do total da memória, ou seja, (totalCache)mod(qtdConjunto) = 0
  if totalCache%qtdConjuntos != 0:
    print('\n\n------------------------------')
    print('ERRO: O número de conjuntos {} deve ser obrigatoriamente um divisor do total de memória cache disponível {}.'.format(qtdConjuntos, totalCache))
    print('------------------------------')
    exit()

  if (politicaSubstituicao == 'AMBAS'):
    executar_mapeamento_associativo_conjunto(totalCache, qtdConjuntos, posicoesMemoriaAcessar, 'FIFO', politica_escrita)
    executar_mapeamento_associativo_conjunto(totalCache, qtdConjuntos, posicoesMemoriaAcessar, 'RANDOM',politica_escrita)
    fim=time.time()
    segundos_total = fim - inicio
    print(tempoExecucao(segundos_total))
  else:
    executar_mapeamento_associativo_conjunto(totalCache, qtdConjuntos, posicoesMemoriaAcessar, politicaSubstituicao, politica_escrita)
    fim=time.time()
    segundos_total = fim - inicio
    print(tempoExecucao(segundos_total))
else:
  print('\n\n------------------------------')
  print('O tipo de mapeamento \'{}\'não foi encontrado. \''.format(tipoMapeamento))
  print('------------------------------')
  exit()


