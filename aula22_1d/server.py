from model import ElFarolModel
import math
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def agent_portrayal(agent):
 
    if agent.attend == 0:
        "person is at home"
        portrayal = {"Shape": "verde.jpg",
                     "Filled": "true",
                     "Layer": 0,
                     "scale": 0.9}
    elif agent.attend == 1:
        " person is at the bar"
        portrayal = {"Shape": "azul.png",
             "Filled": "true",
             "Layer": 0,
             "scale": 0.9}
#    portrayal = {"Shape": "circle",
#                 "Filled": "true",
#                 "Layer": 0,
#                 "Color": "red",
#                 "r": 0.5}

    return portrayal

memory_size = 5
number_strategies = 10
number_persons = 100
overcrowding_threshold = 60
grid_size = round(2 * round(math.sqrt(number_persons))) 

grid = CanvasGrid(agent_portrayal, grid_size, grid_size, 500, 500)

chart = ChartModule([{"Label": "Attendance", "Color": "Black"}])

model_params = {
    "memory_size": UserSettableParameter("slider", "Memory Size", memory_size,
                                         1, 15, 1),
    "number_strategies": UserSettableParameter("slider", "Number of Strategies",
                                               number_strategies, 1, 20, 1),
    "number_persons": UserSettableParameter("slider", "Number of Persons", 
                                            number_persons, 1, 200, 1),
    "overcrowding_threshold": UserSettableParameter("slider", "Overcrowding Threshold", 
                                                    overcrowding_threshold, 1, 120, 1)
}

server = ModularServer(ElFarolModel,
                       [grid, chart],
                       "El Farol Model",
                       model_params)
#server.port = 8521 # The default
server.launch(port = 8523)
#server.launch()
# H0W TO STOP THE SERVER?