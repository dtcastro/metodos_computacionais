"""
11. As questões abaixo pedem para você resolver um exercício usando
recursão. Elas podem ser resolvidas com o apoio do livro “Introduction
to recursive programming - Manuel Rubio Sanchez” [IRP2018]. Todas
essas questões devem ser bem explicadas (e enunciadas), bem
referenciadas e um código deve ser implementado na linguagem de sua
escolha. Você pode e deve abusar a sua solução com o uso de figuras
(quando for o caso).

b) (*) Exercise 7.9 of [IRP2018].
"""

import turtle # um módulo do python para desenho https://docs.python.org/3/library/turtle.html

def hilbert(ordem, tamanho, rotacao):
    if (ordem == 0):
        return

    turtle.left(rotacao)
    
    hilbert(ordem - 1, tamanho, -rotacao)
    #print("tamanho1: " + str(tamanho))
    turtle.forward(tamanho) # conexão entre as curvas
    turtle.left(-rotacao)
    
    hilbert(ordem - 1, tamanho, rotacao)
    #print("tamanho2: " + str(tamanho))

    turtle.forward(tamanho) # conexão entre as curvas
    hilbert(ordem - 1, tamanho, rotacao)

    turtle.left(-rotacao)
    #print("tamanho3: " + str(tamanho))

    turtle.forward(tamanho) # conexão entre as curvas
    hilbert(ordem - 1, tamanho, -rotacao)
    turtle.left(rotacao)

def desenha_quadrado(lado):
    """desenha o contorno do quadrado"""
    #turtle.penup()
    for i in range(4):
        turtle.forward(lado)
        turtle.left(90)
    
if __name__ == '__main__':

    lado = 500 # lado do quadrado que envolve a figura
    ordem_inicial = 7
    tamanho_inicial = lado / (2 ** ordem_inicial) # contando os segmentos nas figuras
    print(tamanho_inicial)
    margem = tamanho_inicial / 2   
    rotacao = 90 # default da curva de Hilbert; a rigor, não precisa ser um parâmetro
    direcao_inicial = 180 # define o direcionamento da curva; opções são 0, 90, 180 e 270

    turtle.home()
    turtle.speed(100)
    print(turtle.screensize())
    largura = 1.2 * lado
    altura = 1.2 * lado
    turtle.screensize(canvwidth = largura, 
                      canvheight = altura)
    
    #turtle.screensize(2000, 2000) => scrolls
    print(turtle.screensize())
    print(turtle.pos())

    turtle.penup()
    turtle.setpos(-lado/2, - lado/2)
    turtle.pendown()
    desenha_quadrado(lado)
    turtle.penup()
    
    #turtle.setpos(-300, -250)
    if direcao_inicial == 0:
        turtle.setpos(-(lado/2 - margem), 
                      -(lado/2 - margem))

    if direcao_inicial == 90:
        turtle.setpos((lado/2 - margem), 
                      -(lado/2 - margem))
    
    if direcao_inicial == 180:
        turtle.setpos((lado/2 - margem), 
                      (lado/2 - margem))

    if direcao_inicial == 270:
        turtle.setpos(-(lado/2 - margem), 
                      (lado/2 - margem))

    # fazer pros demais
    
    turtle.left(direcao_inicial)
    turtle.pendown()

    hilbert(ordem_inicial, tamanho_inicial, rotacao)
    turtle.done()
