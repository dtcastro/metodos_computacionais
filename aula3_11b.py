# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:45:33 2019

@author: dtcas
"""

# TODO
# 1 MAIN
# FUNCAO QUE RECEBE A ORDEM OU LE DA TELA
# TIRAR OS PRINTS
# DIMENSIONAR O TAMANHO DA TELA
# CRIAR UM REPOSITORIO DO GIT


import turtle # um módulo do python para desenho https://docs.python.org/3/library/turtle.html

# funciona pro 2 e quase pro 3 e 4; tem que deixar o tamanho fixo
def hilbert(ordem, tamanho, rotacao):
    if (ordem == 0):
        return

    turtle.left(rotacao)
    
    hilbert(ordem - 1, tamanho, -rotacao)
    print("tamanho1: " + str(tamanho))
    turtle.forward(tamanho)
    turtle.left(-rotacao)
    
    hilbert(ordem - 1, tamanho, rotacao)
    print("tamanho2: " + str(tamanho))

    turtle.forward(tamanho)
    hilbert(ordem- 1, tamanho, rotacao)

    turtle.left(-rotacao)
    print("tamanho3: " + str(tamanho))

    turtle.forward(tamanho)
    hilbert(ordem - 1, tamanho, -rotacao)
    turtle.left(rotacao)

turtle.home()
turtle.speed(10)
print(turtle.screensize())
print(turtle.pos())
turtle.penup()
turtle.setpos(-300, -250)
turtle.pendown()

tamanho_inicial = 100
ordem_inicial = 5
hilbert(ordem_inicial, tamanho_inicial/ordem_inicial, 90)
turtle.done()

#TODO direcionamento inicial
