"""
Exibe o resultado da simulação em um grid no browser.
"""

from model import DLAModel, GREEN_COLOR, RED_COLOR
import math
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
    """
    Define como os agentes devem ser exibidos.
    Agentes verdes são exibidos como retângulos e agentes vermelhos como setas
    direcionados conforme definido em model.py.
    """
    portrayal = {"Filled": "true",
                 "Layer": 0,
                 "Color": "rgb(0,0,0)"}

    if agent.color == GREEN_COLOR:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Color"] = "rgb(0,255,0)"
        
    elif agent.color == RED_COLOR:
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

"700 é o tamanho do grid em pixels"
grid = CanvasGrid(agent_portrayal, grid_size, grid_size, 700, 700)

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
server.launch(port = 8505)


