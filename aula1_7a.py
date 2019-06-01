"""
7. Para resolver as questões abaixo considere o livro "Generative
Art: A Practical Guide Using Processing" por Matt Pearson.
Sugere-se que se use Python, mas admite-se a solução em qualquer
programa que não seja o "Processing" cujas soluções estão
apresentadas no livro. Todas essas questões devem ser bem
explicadas (e enunciadas), bem referenciadas e um código deve ser
implementado na linguagem de sua escolha. Você pode e deve
abusar a sua solução com o uso de 
guras.
a) (*) Replique Figuras 4.7 e 4.8.
p. 74 do livro
"""

import turtle
import math
import random

def ruido(valor, regular):
    """Retorna o ruído com base no valor recebido com parâmetro
    Se o ruído é regular, o valor do ruído é o seno ao cubo.
    Se o ruído não é regular, o valor do ruído é o seno elevado ao resto 
    da divisão inteira por 12 do valor recebido como parâmetro
    """
    if regular:
        return math.pow(math.sin(valor), 3)
    else:
        count = int((valor % 12))
        return math.pow(math.sin(valor), count)
        
def desenha_ruido(raio_regular, regular):
    """Desenha o ruído ao redor do círculo"""
    turtle.pensize(1) # grossura do traço
    turtle.begin_fill() # figura será colorida no final
    
    val_ruido = random.randrange(10) # gera um número aleatório entre 0 e 10
    for i in range(360):
        """Desenha o ruído ao redor do círculo com espaçamento de um grau"""
        val_ruido += 0.1
        raio_variavel = 30 * ruido(val_ruido, regular)
        raio = raio_regular + raio_variavel # a cada iteração é desenhada uma linha com tamanho tamanho do raio regular mais um valor variável
        rads = (i/180) * math.pi # converte de graus para radianos
        x = raio * math.cos(rads)
        y = raio * math.sin(rads)
        
        if (i == 0):
            turtle.penup() # não desenha a linha na primeira movimentação
            x_inicial = x # armazena a posição inicial para fechar a figura
            y_inicial = y
        else: 
            turtle.pendown()        
        
        turtle.setpos(x, y)
        turtle.dot(size = 2)
    
    turtle.setpos(x_inicial, y_inicial) # fecha a figura
    turtle.end_fill()

def desenha_circulo(raio_regular):
    """Desenha o círculo interno da figura"""
    turtle.penup() # para não desenhar a linha na primeira movimentação
    turtle.setpos(0, -raio_regular) # a posição inicial do círculo é a parte mais baixa dele e não o centro
    turtle.pendown()
    turtle.pensize(3) # largura do círculo é maior que a largura do desenho que envolve o circulo
    turtle.circle(raio_regular) # desenha um círculo de raio 100

if __name__ == '__main__':
    # https://ecsdtech.com/8-pages/121-python-turtle-colors
    turtle.color("light gray", "dim gray") # primeira cor é da linha e segunda é do preenchimento
    turtle.speed(10) # seta a velocidade máxima do turtle
    turtle.home()

    raio_regular = 100
    regular = 0 # se 1, o ruido é regular e a figura 4.7 é desenhada; se 0, o ruído não é regular e a figura 4.8 é desenhada
    desenha_ruido(raio_regular, regular)
    desenha_circulo(raio_regular)
    
    turtle.done()
    