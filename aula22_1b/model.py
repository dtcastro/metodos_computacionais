"""
Implementação em Python com o módulo Mesa do modelo DLA do NetLogo:
    Wilensky, U.; Rand, W. (2015). NetLogo DLA model.
    
Documentação do mesa: https://mesa.readthedocs.io/en/master/index.html
Código no GitHub do mesa: https://github.com/projectmesa/mesa

Comentários em inglês são de (Wilensky e Rand, 2015).
"""

import math
import random
from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.space import SingleGrid

GREEN_COLOR = 0 # agentes verdes são parados
RED_COLOR = 1 # agentes vermelhos se movem
    
class Particle(Agent):
    """
    Uma partícula que, se verde não se move e, se vermelha, se move
    aleatoriamente até tocar uma partícula verde e parar de se mover.
    Partículas vermelhas são exibidas como setas vermelhas no arquivo
    server.py, direcionadas de acordo com o atributo heading.
    
    Uma possibilidade seria implementar duas classes de agentes, uma para os 
    vermelhos e uma para os verdes, já que para os verdes importa apenas os 
    atributos color e pos.
    """
    def __init__(self, unique_id, model, color, heading, pos):
        super().__init__(unique_id, model)
        self.color = color # pode ser vermelho ou verde
        self.heading = heading # direção da seta
        self.pos = pos # posição do agente
        self.angle = 0 # ângulo para o qual a partícula vermelha está direcionada
        
    def __str__(self):
        return "Particle %d" % (self.unique_id)
     
    def set_angle(self):
        """
        Determina o ângulo para o qual a partícula vermelha está direcionada,
        com base no heading. 
        Os valores de heading poderiam ser constantes em uma evolução do código.
        """
        if (self.heading == (1, 0)): # direita -> angulo 0
            self.angle = 0
        elif (self.heading == (0, 1)): # cima -> angulo 90
            self.angle = 90            
        elif (self.heading == (-1, 0)): # esquerda -> angulo 180
            self.angle = 180            
        elif (self.heading == (0, -1)): # baixo -> angulo 270
            self.angle = 270            

    def set_heading(self):
        """
        Determina o heading para o qual a partícula vermelha está direcionada,
        com base no ângulo.
        Os valores de heading poderiam ser constantes em próxima versão do 
        código.
        """
        if (self.angle >= 315 or self.angle < 45):
            self.heading = (1, 0) # direita
        elif (self.angle >= 45 and self.angle < 135):
            self.heading = (0, 1) # cima
        elif (self.angle >= 135 and self.angle < 225):
            self.heading = (-1, 0) # esquerda
        elif (self.angle >= 225 and self.angle < 315): 
            self.heading = (0, -1) # baixo
    
    def determine_new_position(self):
        """
        Determina para qual vizinho a partícula vermelha se moverá, com base
        no ângulo para o qual está direcionada.
        """
        if (self.angle >= 338 or self.angle < 23):
            new_position = (self.pos[0] + 1, self.pos[1]) # leste
        elif (self.angle >= 23 and self.angle < 68):
            new_position = (self.pos[0] + 1, self.pos[1] + 1) # nordeste
        elif (self.angle >= 68 and self.angle < 113):
            new_position = (self.pos[0], self.pos[1] + 1) # norte
        elif (self.angle >= 113 and self.angle < 158): 
            new_position = (self.pos[0] - 1, self.pos[1] + 1) # noroeste
        elif (self.angle >= 158 and self.angle < 203): 
            new_position = (self.pos[0] - 1, self.pos[1]) # oeste
        elif (self.angle >= 203 and self.angle < 248): 
            new_position = (self.pos[0] - 1, self.pos[1] - 1) # sudoeste
        elif (self.angle >= 248 and self.angle < 293): 
            new_position = (self.pos[0], self.pos[1] - 1) # sul
        elif (self.angle >= 293 and self.angle < 338): 
            new_position = (self.pos[0] + 1, self.pos[1] - 1) # sudeste
        
        " verifica se a posição é válida, já que as coordenadas podem ser "
        " passado do limite do grid para mais ou para menos"
        if (new_position[0] >= self.model.grid.width):
            new_position = (0, new_position[1])
        if (new_position[0] < 0):
            new_position = (self.model.grid.width - 1, new_position[1])
        if (new_position[1] >= self.model.grid.height):
            new_position = (new_position[0], 0)
        if (new_position[1] < 0):
            new_position = (new_position[0], self.model.grid.height - 1)

        return new_position
        
    def move(self):
        """
        Desloca uma partícula vermelha aleatoriamente, primeiro direcionando-a
        aleatoriamente para a direita e depois para a esqueda. Com base na 
        direção, vai a para o vizinho apropriado, se estiver vazio. Se o 
        vizinho estiver ocupado, não se move, mas muda a direção.
        """
        right = random.randrange(0, self.model.wiggle_angle)
        left = random.randrange(0, self.model.wiggle_angle)
        self.set_angle()
        self.angle -= right
        self.angle +- left
        if self.angle < 0:
            self.angle += 360
        
        new_position = self.determine_new_position()
        " verifica se o vizinho apropriado está vazio antes de mover"
        " se o vizinho estiver ocupado, não se move"
        if (self.model.grid.is_cell_empty(new_position)):
            self.model.grid.move_agent(self, new_position)
            self.pos = new_position

        self.set_heading()

    def move_alternative(self):
        """
        MÉTODO DE DESLOCAMENTO ALTERNATIVO; NÃO ESTÁ SENDO USADO.
        Desloca as partículas vermelhas aleatoriamente; tem o mesmo efeito do 
        código do NetLogo, mas é mais simples porque escolhe aleatoriamente
        um dos vizinhos da posição atual da partícula vermelha para ir. No 
        NetLogo, a direção de deslocamente é mais fácil de implementar que no
        Mesa.
        """
        
        " retorna uma lista com as posições dos vizinhos da partícula,"
        " como tuplas no formato (x, y)"
        possible_steps = self.model.grid.get_neighborhood(self.pos,
            moore = True, include_center = False)
        
        total_number_neighbors = 8 # são oito vizinhos, contando com as diagonais

        for i in range(total_number_neighbors):
            " tenta se algum dos oito vizinhos está vazio; desloca-se para o" 
            " primeiro vizinho vazio"
            new_position = self.random.choice(possible_steps)
            if (self.model.grid.is_cell_empty(new_position)):
                self.model.grid.move_agent(self, new_position)
                self.pos = new_position
                break
    
    def step(self):
        """ 
        Passo da extensão 2. Desloca as partículas apenas se forem vermelhas.
        Dependendo da probabilidade de grudar, a partícula muda para o tipo
        verde, se ela tiver tocado em outra partícula verde.
        """
      
        if self.color == RED_COLOR:
            self.move()
            
            "recupera a lista de vizinhos verdes da partícula, já na nova"
            "posição"
            green_neighbors = [neighbor for neighbor in 
                               self.model.grid.iter_neighbors(self.pos, 
                                                              moore = True)
                               if neighbor.color == GREEN_COLOR]

            number_green_neighbors = len(green_neighbors)
            "oito vizinhos no total, contando com as diagonais"
            total_number_neighbors = 8
            
            if self.model.neighbor_influence:
                "Comentário de Wilensky e Rand (2015):"
                "if neighbor-influence is TRUE then make the probability" 
                "proportionate to the number of green neighbors, otherwise"
                "use the slider as before"
                "increase the probability of sticking the more green neighbors"
                "there are"
                local_prob = self.model.probability_of_sticking * \
                    number_green_neighbors/total_number_neighbors
            else:
                local_prob = self.model.probability_of_sticking
            
            if number_green_neighbors > 0:
                "se algum dos vizinhos da nova posição, muda de cor com a"
                "probabilidade calculada acima"
                random_number = random.uniform(0, 1)
                if (random_number < local_prob):
                    self.color = GREEN_COLOR

    def step_original_and_extension1(self):
        """
        PASSO DO MODELO ORIGINAL E DA EXTENSÃO 1; NÃO ESTÁ SENDO USADO.
        """
        if self.color == RED_COLOR:
            self.move()
            
            for neighbor in self.model.grid.iter_neighbors(self.pos, 
                                                           moore = True):
                if neighbor.color == GREEN_COLOR:
                    # modelo original
                    #self.color = GREEN_COLOR
                    
                    # modelo da extensão 1
                    random_number = random.uniform(0, 1)
                    if (random_number < self.model.probability_of_sticking):
                        self.color = GREEN_COLOR
                    break


class DLAModel(Model):
    """
    Modelo DLA como implementado no NetLogo.
    """
    def __init__(self, wiggle_angle, number_particles, probability_of_sticking, 
                 neighbor_influence, num_seeds):
        self.running = True # necessário para que o modelo seja chamado pelo servidor web
        self.wiggle_angle = wiggle_angle
        self.number_particles = number_particles
        " indica com que probabilidade uma partícula vermelha se torna verde " 
        " e pára ao tocar uma partícula verde"
        self.probability_of_sticking = probability_of_sticking
        "indica se o número de vizinhos verdes influencia a probabilidade de"
        "grudar"
        self.neighbor_influence = neighbor_influence
        if num_seeds <= 0: # número de sementes deve ser positivo
            raise ValueError("Number of seeds should be greater than zero.")
        self.num_seeds = num_seeds
        "direções das particulas"
        "(1,0) direita; (0, 1) cima; (-1, 0) esquerda (0, -1) baixo"
        self.headings = ((1, 0), (0, 1), (-1, 0), (0, -1))
        self.schedule = BaseScheduler(self)

        "tamanho do grid definido em função do número de partículas, como na" 
        "visualização; pode ser um valor comum aos dois"
        width = height = round(2 * round(math.sqrt(number_particles)))
        
        "apenas um agente por célula"
        self.grid = SingleGrid(width, height, True)
        
        "Cria as sementes"
        for i in range(self.num_seeds):
            if self.num_seeds == 1:
                """
                Coloca a semente no centro do grid. O modelo final do NetLogo,
                com a extensão 3, não coloca uma semente unitária no centro,
                mas em uma posição aleatória também.
                """
                x = round(self.grid.width / 2);
                y = round(self.grid.height / 2);
                "o angulo e o a probabilidade de colar não são relevantes, já" 
                "que as sementes não se movem"
                particle = Particle(i, self, GREEN_COLOR, 0, (x, y))
                self.grid.place_agent(particle, (x, y))
            else:
                """
                Coloca as sementes em posições aleatórias. A posição 
                será atribuída pelo método position_agent
                """
                particle = Particle(i, self, GREEN_COLOR, 0, (0, 0))
                self.grid.position_agent(particle)
            
            self.schedule.add(particle)

        "Cria as partículas"
        for i in range(self.number_particles):
           
            "a posição será atribuída pelo método position_agent"
            heading = self.random.choice(self.headings)
            particle = Particle(i, self, RED_COLOR, heading, (0, 0))
            self.grid.position_agent(particle)
            self.schedule.add(particle)
        
    def step(self):
        """
        Avança o modelo em um passo.
        """
        self.schedule.step()
