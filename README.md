# algebra-a

Durante a disciplina Álgebra A, pesquisei e agrupei alguns algoritmos que pudessem ser úteis nos estudos e melhor compreensão da matéria. Aqui constam as respectivas implementações e o cabeçalho de cada função relacionada. Para maiores informações, leia o arquivo al.py

## Instruções de uso
Navegue até a pasta onde está o arquivo al.py

```
$ python3
>>> import al
>>> al.funcao(a,b)
```

## Observações
1. Se durante um exercicio de interpolação de Lagrange, por ex, chegar a um termo do tipo A/B, lembrar que mod n, A/B equivale a A * B^(-1), ou seja, A * inverso de B em Zn.

## Funções presentes na implementação

### Primos 

##### ehPrimo(p)
Teste de primalidade simples.

##### lucasLehmer(p)
Teste de Lucas-Lehmer para detectar números de Mersenne primos.

##### mersennePrimo(n)
Verifica se um numero primo n gera um número de Mersenne primo.

### Aritmetica modular

##### mdc(a, b)
Algoritmo euclideano simples, utilizado para calcular o mdc(a,b).

##### mdce(a, b, 1, __verbose = False)
Algoritmo euclideano estendido, utilizado para calcular os valores das constantes alfa e beta que satifazem equações da forma:

a * alfa + b * beta = mdc(a,b)

r | q | x | y       
a | * | 1 | 0
b | * | 0 | 1

Essa função pode ter um quarto parâmetro (opcional) "True" ou "False", indicando que deve ou não imprimir na tela o passo-a-passo do procedimento.

##### modinv(a, n, 1, __verbose = False)
Recupera o inverso multiplicativo de 'a' na base 'n' utilizando o algoritmo euclidiano estendido. Essa função pode ter um quarto parâmetro (opcional) "True" ou "False", indicando que deve ou não imprimir na tela o passo-a-passo do procedimento.

##### expmod(base, exp, modulo)
Função para calcular grandes potencias módulo n. 

### Grupos

##### totiente(n)
Conta quantos elementos em Zn são coprimos a n.
Popularmente conhecida como função fi de n.

##### achaExpoente(a, n, fi, __mod = 1)
Calcula o menor expoente 'x' necessário para que expmod(a, x, n) seja igual a __mod. Caso __mod não seja informado, cai no caso especial em que calcula a menor potência para que expmod(a, x, n) seja igual a 1, calculando portanto a ordem do elemento a em Zn.

Essa função aceita um quarto parâmetro (opcional) cujo valor padrão é 1. Esse parâmetro serve para avaliar o expoente x necessário para que a ^ x % n seja congruente a "__mod"

##### eCiclico(n)
Verifica se um grupo é cíclico calculando sua ordem e a de todos os seus elementos.

### RSA

##### encripta(mensagem, e, n)
Encripta um bloco da mensagem por meio da exponenciação modular com a chave pública.

##### desencripta(mensagem, d, n)
Desencripta um bloco da mensagem por meio da exponenciação modular com a chave privada.

##### geraChaves(n, fi)
Obtém chaves pública e privada para um número n = p * q.

##### cripto(mensagem)
Dado um segredo guardado na variável 'mensagem', a função efetua a cifra do bloco de informações segundo as etapas do RSA.
