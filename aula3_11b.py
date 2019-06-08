"""
Created on Sun May 12 22:45:33 2019

@author: dtcas
"""

import turtle # um módulo do python para desenho https://docs.python.org/3/library/turtle.html

def hilbert(ordem, tamanho, rotacao):
    if (ordem == 0):
        return

    turtle.left(rotacao)
    
    hilbert(ordem - 1, tamanho, -rotacao)
    #print("tamanho1: " + str(tamanho))
    turtle.forward(tamanho)
    turtle.left(-rotacao)
    
    hilbert(ordem - 1, tamanho, rotacao)
    #print("tamanho2: " + str(tamanho))

    turtle.forward(tamanho)
    hilbert(ordem - 1, tamanho, rotacao)

    turtle.left(-rotacao)
    #print("tamanho3: " + str(tamanho))

    turtle.forward(tamanho)
    hilbert(ordem - 1, tamanho, -rotacao)
    turtle.left(rotacao)

if __name__ == '__main__':

    tamanho_inicial = 50 # comprimento do segmento para a curva de ordem 1; 
    # ordens maiores usam segmentos proporcionalmente menores
    ordem_inicial = 6
    rotacao = 90 # default da curva de Hilbert; a rigor, não precisa ser um parâmetro
    direcao_inicial = 270 # define o direcionamento da curva; opções são 0, 90, 180 e 270
    margem = 0.1 * tamanho_inicial * ordem_inicial # distância que o desenho deve estar dos limites da janela

    turtle.home()
    turtle.speed(100)
    print(turtle.screensize())
    turtle.screensize(canvwidth = tamanho_inicial * ordem_inicial + margem, 
                      canvheight = tamanho_inicial * ordem_inicial + margem)
    
    #turtle.screensize(2000, 2000) => scrolls
    print(turtle.screensize())
    print(turtle.pos())
    turtle.penup()
    #turtle.setpos(-300, -250)
    if direcao_inicial == 0:
        turtle.setpos(-(tamanho_inicial * ordem_inicial - margem), 
                      -(tamanho_inicial * ordem_inicial - margem))

    if direcao_inicial == 90:
        turtle.setpos((tamanho_inicial * ordem_inicial - margem), 
                      -(tamanho_inicial * ordem_inicial - margem))
    
    if direcao_inicial == 180:
        turtle.setpos((tamanho_inicial * ordem_inicial - margem), 
                      (tamanho_inicial * ordem_inicial - margem))

    if direcao_inicial == 270:
        turtle.setpos(-(tamanho_inicial * ordem_inicial - margem), 
                      (tamanho_inicial * ordem_inicial - margem))

    # fazer pros demais
    
    turtle.left(direcao_inicial)
    turtle.pendown()

    hilbert(ordem_inicial, tamanho_inicial/ordem_inicial, rotacao)
    turtle.done()
