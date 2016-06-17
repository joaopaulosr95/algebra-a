#/usr/bin/python

from random import randrange
from sys import stdout
from math import sqrt, log

# -------------------------------------------- #
# Primos
# -------------------------------------------- #

def ehPrimo(p):

    """
        Teste de primalidade simples
    """
    if p == 2:
        return True
    elif p <= 1 or p % 2 == 0: 
        return False
    else:
        # Apenas impares ate a raiz de p
        for i in range(3, int(sqrt(p)) + 1, 2): 
            if p % i == 0:
                return False
        return True

def lucasLehmer(p):

    """
        Teste de Lucas-Lehmer para detectar numeros de Mersenne primos
    """
    if p == 2:
        return True
    
    # 2 ^ p - 1
    mersenne = ( 1 << p ) - 1

    print("M(%d) = %d" % (p, mersenne))

    s = 4
    print ("S0 = %d" % (s))

    for i in range(1, p - 1):
        print("S%d = (%d ** 2 - 2) (mod %d) = %d (mod %d)" % \
                (i, s, mersenne, ((s ** 2 - 2) % mersenne), mersenne))
        s = ((s ** 2) - 2) % mersenne

    if s == 0:
        return True
    else:
        return False

def mersennePrimo(n):

    """
        Verifica se um numero primo n gera um numero de Mersenne primo
    """
    if ehPrimo(n) and lucasLehmer(n):
        return ("%d e primo e M(%d) tambem e primo" % (n, n)) 
    elif not ehPrimo(n):
        return ("%d nao e primo" % (n))
    elif not lucasLehmer(n):
        return ("M(%d) nao e primo" % ((1 << n) - 1))

# -------------------------------------------- #
# Aritmetica modular
# -------------------------------------------- #

def mdc(a, b):

    """
        Algoritmo euclideano simples, utilizado para calcular o mdc(a,b)
    """
    if (a == 0 or b == 0):
        return 0

    # Garante que o primeiro parametro e sempre maior que o segundo
    if (a < b):
        a,b = b,a

    if a % b == 0:
        return b
    else:
        return mdc(b, a % b)

def mdce(aa, bb, __verbose = False):

    """
        Algoritmo euclideano estendido, utilizado para calcular os 
        valores das constantes alfa e beta que satifazem equacoes 
        da forma 
        a * alfa + b * beta = mdc(a,b)

        r   |	q   |	x   |	y	
        a   |	*   |	1   |	0
        b   |	*   |	0   |	1
        (...)			
    """
    a = aa
    b = bb
    swap = False

    # Garante que o primeiro parametro seja maior que o segundo
    if (a < b):
        a, b = b, a
    swap = True

    x = [1, 0]
    y = [0, 1]

    if __verbose:
        print("%d\t*\t%d\t%d" % (a, x[0], y[0]))
        print("%d\t*\t%d\t%d" % (b, x[1], y[1]))

    while a % b != 0:
        q, r = a // b, a % b
        """ 
            Calculo dos novos valores para x e y 
            x0 <- x1
            x1 <- Ultimo valor de x0 - x1 * q
            (Processo analogo para y) 
        """

        x[0], x[1] = x[1], x[0] - x[1] * q
        y[0], y[1] = y[1], y[0] - y[1] * q

        if __verbose:
            print("%d\t%d\t%d\t%d" % (r, q, x[1], y[1]))

        a, b = b, r

    """ 
        Caso os parametros 'a' e 'b' tenham sido trocados, vamos 
        inverter os respectivos valores de 'alfa' e 'beta' 
    """
    if swap == False:
        if __verbose:
            print("\n%d * (%d) + %d * (%d) = %d\n" % \
                    (aa, x[1], bb, y[1], b))
        return b, x[1], y[1]
    else:
        if __verbose:
            print("\n%d * (%d) + %d * (%d) = %d\n" % \
                    (aa, y[1], bb, x[1], b))
        return b, y[1], x[1]

def modinv(a, n, __verbose = False):

    """  
        Recupera o inverso multiplicativo de 'a' na base 'n' 
        utilizando o algoritmo euclidiano estendido
    """
    while a < 0:
        a += n

    mdc, alfa, beta = mdce(a, n, __verbose)
    if mdc != 1:
        return 0
    return alfa % n

def expmod(base, exp, modulo):

    """
        Funcao para calcular grandes potencias modulo n
        Recebe como parametros a base, o expoente e o modulo
    """
    if (base == modulo):
        return 0
    
    # Pequeno teorema de fermat
    elif (ehPrimo(modulo) and exp == modulo - 1):
        return 1
    elif (ehPrimo(modulo) and exp == modulo):
        return base

    resultado = 1 
    while exp > 0:
        if exp % 2 == 1:
            resultado = resultado * base % modulo
            exp = exp >> 1
            base = base * base % modulo

    return resultado

# -------------------------------------------- #
# Grupos
# -------------------------------------------- #

def totiente(n):

    """ 
        Conta quantos elementos em Zn sao coprimos a n.
        Popularmente conhecida como funcao fi de n.
    """
    fi = 0
    for i in range(1, n):
        if mdc(i, n) == 1:
            fi += 1

    return fi

def achaExpoente(a, n, fi, __mod = 1):

    """
        Calcula o menor expoente 'x' necessario para que 
        expmod(a, x, n) seja igual a __mod.
        Caso mod nao seja informado, cai no caso especial
        em que calcula a menor potencia para que
        expmod(a, x, n) seja igual a 1, calculando portanto
        a ordem do elemento a em Zn.
    """

    if __mod == 1:
        if a > n:
            a = a % n
        if a == 0:
            return 0
        elif a == 1:
            return 1

    for i in range(2, fi + 1):
        if expmod(a, i, n) == 1:
            return i
    return -1

def eCiclico(n):

    """
        Verifica se um grupo e ciclico calculando sua ordem
        e a de todos os seus elementos
    """
    fi = totiente(n)
    print("fi = %d" % fi)

    if ehPrimo(n):
        ciclico = True
    else:
        ciclico = False

    geradores = []
    maiorElemento = 0
    maiorOrdem = 0

    for i in range(1, fi + 1):
        ordem = achaExpoente(i, n, fi)
        if ordem == fi:
            geradores.append(i)

        if ordem > maiorOrdem:
            maiorElemento = i
            maiorOrdem = ordem

        if ordem == -1:
            print("%d, ordem INFINITO" % (i))
        else:
            print("%d, ordem %d" % (i, ordem))

    if (ciclico == True):
        print("Grupo ciclico! Seus geradores sao: ")
        print(geradores)
    else:
        print("Grupo nao e ciclico, o elemento de maior ordem e %d, \
                cuja ordem e %d" % (maiorElemento, maiorOrdem))

def representantes(n):

    """
        Teorema de Lagrange: A ordem de qualquer representante de Zn
        deve dividir a ordem do grupo
    """
    fi = totiente(n)

    # Primeiro vamos obter a lista de possiveis ordens
    divisores = []
    for i in range(1, fi+1):
        if fi % i == 0:
            divisores.append(i)

    # Agora vamos buscar os elementos que possuem as ordens encontradas
    for x in divisores:
        representantes = []
        print("Representantes da ordem %d: \n" %(x))
        for i in range (1, fi+1):
            if achaExpoente(i, n, fi) == x:
                representantes.append(i)
        print(representantes)

# -------------------------------------------- #
# RSA
# -------------------------------------------- #

def encripta(mensagem, e, n):

    """ 
        Encripta um bloco da mensagem por meio da exponenciacao 
        modular com a chave publica
    """
    return expmod(mensagem,e,n)

def desencripta(mensagem, d, n):

    """ 
        Desencripta um bloco da mensagem por meio da exponenciacao 
        modular com a chave privada
    """
    return expmod(mensagem,d,n)

def geraChaves(n, fi):

    """
        A partir de um numero n e do 'fi de n' gera uma chave 
        publica 'e' e uma chave privada 'd'
    """
    # Gera um numero aleatorio 'e' invertivel modulo 'fi de n'
    while True:
        e = randrange(1, fi - 1)
        if mdc(e, fi) == 1:
            break

    """
        Calcula entao o numero 'd' (chave privada) que seja coprimo ao 
        numero 'e' modulo 'fi de n' 
    """
    d = modinv(e, fi)

    return e, d

def cripto(mensagem):

    """
        Por questoes de praticidade de implementacao esse programa 
        utiliza como base a tabela ASCII
    """
    print("***** SIMULADOR RSA *****")

    """
        Toma dois primos 'p' e 'q' aleatoriamente baseado no teto 
        especificado 
    """
    teto = 5000

    print("Gerando numeros p e q")
    while True:
        p = randrange(1, teto)
        q = randrange(1, teto)
        if p != q and ehPrimo(p) and ehPrimo(q):
            break

    # Efetua entao o produto entre 'p' e 'q'
    n = p * q
    print("\nn = %d * %d" % (p, q))

    """ 
        Calcula a funcao totiente de 'n'. Dado que n e composto por
        dois primos, seu fi vale (p - 1) * (q - 1) 
    """
    fi = (p - 1) * (q - 1)

    # Gera as chaves publica e privada
    print ("Gerando chaves publica e privada...")
    e, d = geraChaves(n, fi)

    print ("\nChave publica (n, e): (%d, %d)" % (n, d)) 
    print ("Chave privada (n, d): (%d, %d)" % (n, e))

    # Etapa de encriptacao:
    print("\nEncriptando a mensagem...")
    encriptada = [ encripta(ord(x), e, n) for x in mensagem ]
    print ("\nA mensagem cifrada em blocos vira: " 
            + ''.join([str(x) for x in encriptada]))

    # Etapa de desencriptacao
    print ("\nDesencriptando a mensagem...")
    desencriptada = [ chr(desencripta(x, d, n)) for x in encriptada ]
    print ("\nA mensagem desencriptada virou: " + desencriptada)
