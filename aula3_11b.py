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

import turtle # módulo do python para desenho https://docs.python.org/3/library/turtle.html

def hilbert(ordem, tamanho, rotacao):
    """
    Desenha segmento da curva de hilbert com ordem e tamanho recebidos como
    parâmetro; o parâmetro rotação indica para que direção a tartaruga virará
    A cada chamada recursiva da função, a ordem é reduzida até a condição de
    parada.
    """
    if (ordem == 0):
        return

    turtle.left(rotacao)
    hilbert(ordem - 1, tamanho, -rotacao)
 
    turtle.forward(tamanho) # conexão entre as curvas

    turtle.left(-rotacao)
    hilbert(ordem - 1, tamanho, rotacao)
 
    turtle.forward(tamanho) # conexão entre as curvas

    hilbert(ordem - 1, tamanho, rotacao)
    turtle.left(-rotacao)
 
    turtle.forward(tamanho) # conexão entre as curvas

    hilbert(ordem - 1, tamanho, -rotacao)
    turtle.left(rotacao)

def desenha_quadrado(lado):
    """
    Desenha o quadrado que emoldura a curva de Hilbert
    """
    for i in range(4):
        turtle.forward(lado)
        turtle.left(90)
    
if __name__ == '__main__':

    lado = 500 # lado do quadrado que envolve a curva de Hilbert
    ordem_curva = 6 # ordem da curva de Hilbert
    tamanho_segmento = lado / (2 ** ordem_curva) # quanto maior a ordem da curva,
    # menor o tamanho do segmento; na figura do ex 7.9, o lado do quadrado é
    # dividido por 2 elevado à ordem da curva para se chegar ao tamanho do
    # segmento, incluindo as margens, correspondentes à metade de um segmento 
    # em cada lado
    margem = tamanho_segmento / 2   
    rotacao = 90 # default da curva de Hilbert; a rigor, não seria um parâmetro
    direcao_curva = 180 # define o direcionamento da curva; 
    # opções são 0 (U para baixo), 90 (C), 180 (U) e 270 graus (C ao contrário)

    turtle.home()
    turtle.speed(100) # velocidade da tartaruga
    # definição do tamanho da janela
    largura_janela = 1.2 * lado
    altura_janela = 1.2 * lado
    turtle.screensize(canvwidth = largura_janela, canvheight = altura_janela)

    turtle.penup()
    # a janela é dividia em quatro por dois eixos cartesianos, com o zero na 
    # interseção; o quadrado será centralizado 
    turtle.setpos(-lado/2, -lado/2)
    turtle.pendown()
    desenha_quadrado(lado)
    turtle.penup()
    
    # define a posição para início do desenho da curva, com base na direção da 
    # curva; a curva é desenhada dentro do quadrado, respeitando a margem
    # definida
    if direcao_curva == 0: # curva virada para baixo (U de cabeça para baixo)
        turtle.setpos(-(lado/2 - margem), -(lado/2 - margem)) # a curva é 
        # desenhada a partir do 3o. quadrante no sentido horário
    elif direcao_curva == 90: # curva virada para a direita (como na letra C)
        turtle.setpos((lado/2 - margem), -(lado/2 - margem)) # a curva é 
        # desenhada a partir do 4o. quadrante no sentido horário
    elif direcao_curva == 180: # curva virada para cima (como na letra U)
        turtle.setpos((lado/2 - margem), (lado/2 - margem)) # a curva é 
        # desenhada a partir do 1o. quadrante no sentido horário
    elif direcao_curva == 270: # curva virada para a esqueda (letra C ao contrário)
        turtle.setpos(-(lado/2 - margem), (lado/2 - margem)) # a curva é
        # desenhada a partir do 2o. quadrante no sentido horário
    else:
        turtle.done()
        raise ValueError("Opções devem ser 0, 90, 180 ou 270")

    turtle.left(direcao_curva)
    turtle.pendown()
    hilbert(ordem_curva, tamanho_segmento, rotacao)
    turtle.done()
    turtle.exitonclick()