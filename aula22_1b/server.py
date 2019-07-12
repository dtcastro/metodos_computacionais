"""
Exibe o resultado da simulação em um grid no browser.
"""

from model import DLAModel, GREEN_COLOR, RED_COLOR
import math
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

class NumberGreenElement(TextElement):
    """
    Exibe os valores máximo, mínimo e médio de recompensas dos agentes,
    calculados no método step do modelo.
    """
    def __init__(self):
        pass

    def render(self, model):
        return "Number of green particles: {}<br>Number of red particles: \
                {}".format(model.number_green_particles, 
                model.number_particles - model.number_green_particles)

def agent_portrayal(agent):
    """
    Define como os agentes devem ser exibidos.
    O modelo do NetLogo representa os agentes como pessoas estilizadas. Para 
    fazer algo semelhante com o módulo mesa, é necessário que os agentes sejam exibidos
    como imagens. O código alternativo comentado ao final do método faz isso,
    mas dessa forma não é possível exibir as tonalidades representando o nível
    de recompensas. Dessa forma, a opção foi representar os agentes como 
    quadrados, sendo a cor definida em função do valor das recompensas.
    A localização de cada agente é definida no modelo, com o bar no quadrante 
    superior direito do grid. Os agentes no bar são exibidos em azul e os 
    agentes em casa são exibidos em verde para tentar manter a lógica do modelo
    do NetLogo, já que parece não ser possível exibir no módulo mesa o próprio 
    grid em cores específicas.
    """
#    portrayal = {"Shape": "rect", # agentes são exibidos como quadrados
#                 "w": 0.5, # altura de 50% do tamanho da célula
#                 "h": 0.5, # largura de 50% do tamanho da célula
#                 "Filled": "true",
#                 "Layer": 0,
#                 "Color": "rgb(0,0,0)"}

    portrayal = {"Filled": "true",
                 "Layer": 0,
                 "Color": "rgb(0,0,0)"}

    # PRIMEIRA EXTENSÃO
    # varia a tonalidade da cor em função do valor das recompensas de cada 
    # agente; 255 é a tonalidade mais clara; 0 é a tonalidade mais escura
    # no NetLogo as tonalidades parecem variar de forma mais elástica
    
    if agent.color == GREEN_COLOR:
        # os agentes fora do bar são exibidos em tonalidades de verde
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Color"] = "rgb(0,255,0)"
        
    elif agent.color == RED_COLOR:
        # os agentes dentro do bar são exibidos em tonalidades de azul
        portrayal["Shape"] = "arrowHead"
        portrayal["scale"] = 0.8
        portrayal["heading_x"] = agent.heading[0]
        portrayal["heading_y"] = agent.heading[1]
        portrayal["Color"] = "rgb(255,0,0)"

    return portrayal
    

wiggle_angle = 60
number_particles = 2500
probability_of_sticking = 1
neighbor_influence = False
num_seeds = 1
grid_size = round(2 * round(math.sqrt(number_particles))) 

#reward_element = RewardElement()
# 500 é o tamanho do grid em pixels
grid = CanvasGrid(agent_portrayal, grid_size, grid_size, 700, 700)
#chart = ChartModule([{"Label": "Attendance", "Color": "Black"}])

model_params = {
    "wiggle_angle": UserSettableParameter("slider", "Wiggle Angle",
                                               wiggle_angle, 0, 100, 1),

    "number_particles": UserSettableParameter("slider", "Number of Particles",
                                               number_particles, 1, 5000, 1),
    "probability_of_sticking": 
        UserSettableParameter("slider", "Probability of Sticking Probability",
                              probability_of_sticking, 0, 1, 0.05),
    "neighbor_influence": 
        UserSettableParameter("checkbox", "Neighbor Influence",
                              neighbor_influence),
    "num_seeds": 
        UserSettableParameter("slider", "Number of Seeds",
                              num_seeds, 1, 10, 1)
}

server = ModularServer(DLAModel,
                       [grid],
                       "DLA Model",
                       model_params)

# porta 8521 é a porta default
server.launch(port = 8507)


