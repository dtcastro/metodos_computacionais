"""
Exibe o resultado da simulação em um grid no browser.
"""

from model import ElFarolModel
import math
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

class CrowdedElement(TextElement):
    """
    Exibe o "Crowded" sobre oquadrante superior direito, que representa o bar,
    caso o número de pessoas no bar seja superior ao limite. O texto "Not 
    Crowded" é exibido caso contrário. Aparentemente, não é possível exibir o 
    texto sobre o grid, como acontece no modelo original do NetLogo.
    """

    def __init__(self):
        pass

    def render(self, model):
        # espaços em branco foram adicionados ad hoc para que o texto seja 
        # exibido no quadrante superior direito, que representa o bar; sem os 
        # espaços, o texto é exibido no começo do 
        white_lines = ""
        white_spaces = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        if model.attendance > model.overcrowding_threshold:
            return white_lines + white_spaces + "Crowded"
        else:
            return white_lines + white_spaces + "Not Crowded"

class RewardElement(TextElement):
    """
    Exibe os valores máximo, mínimo e médio de recompensas dos agentes,
    calculados no método step do modelo.
    """
    def __init__(self):
        pass

    def render(self, model):
        return "Max reward: {}<br>Mean reward: {}<br>Min reward: \
                {}".format(model.max_reward, model.mean_reward, 
                model.min_reward)

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
    portrayal = {"Shape": "rect", # agentes são exibidos como quadrados
                 "w": 0.5, # altura de 50% do tamanho da célula
                 "h": 0.5, # largura de 50% do tamanho da célula
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "rgb(0,0,0)",
                 "text": agent.reward, # exibe o valor da recompensa de cada agente
                 "text_color": "white"}

    # PRIMEIRA EXTENSÃO
    # varia a tonalidade da cor em função do valor das recompensas de cada 
    # agente; 255 é a tonalidade mais clara; 0 é a tonalidade mais escura
    # no NetLogo as tonalidades parecem variar de forma mais elástica
    color = 255 - agent.reward if 255 - agent.reward > 0 else 0 
    
    if agent.attend == 0:
        # os agentes fora do bar são exibidos em tonalidades de verde
        portrayal["Color"] = "rgb(0," + str(color) + ",0)"
        
    elif agent.attend == 1:
        # os agentes dentro do bar são exibidos em tonalidades de azul
        portrayal["Color"] = "rgb(0,0," + str(color) + ")"

    return portrayal
    
    # Código alternativo para exibir imagens representando os agentes.
    # O problema é que não é possível exibir as tonalidade representando as
    # as recompensas, a não ser que haja uma imagem para cada tonalidade.
    # O código abaixo tenta associar a escala da imagem ao nível de recompensas,
    # mas o resultado final não é muito bom e optei por exibir os agentes como
    # retângulos, no código final acima

#    if agent.attend == 0:
#        "person is at home"
#        portrayal = {"Shape": "verde.jpg",
#                "Filled": "true",
#                "Layer": 0,
#                # FIRST EXTENSION; original is scale: 0.9
#                "scale": agent.relative_reward if agent.relative_reward > 0 else 0.1}
#        
#    elif agent.attend == 1:
#        " person is at the bar"
#        portrayal = {"Shape": "azul.png",
#             "Filled": "true",
#             "Layer": 0,
#             # FIRST EXTENSION; original is scale: 0.9
#             "scale": agent.relative_reward if agent.relative_reward > 0 else 0.1}

memory_size = 5
number_strategies = 10
number_persons = 100
overcrowding_threshold = 60
# tamanho do grid definido em função do número de pessoas
grid_size = round(2 * round(math.sqrt(number_persons))) 

crowded_element = CrowdedElement()
reward_element = RewardElement()
# 500 é o tamanho do grid em pixels
grid = CanvasGrid(agent_portrayal, grid_size, grid_size, 500, 500)
chart = ChartModule([{"Label": "Attendance", "Color": "Black"}])
# esse histograma mostra o valor das recompensas de cada agente
# a extensão três do NetLogo, diferentemente, mostra quantos agentes têm
# determinado valro de recompensas, do mínimo ao máximo
hist_agents_reward = BarChartModule([{"Label": "Reward", "Color": "Black"}],
                           scope = "agent",
                           sorting = "ascending",
                           sort_by = "unique_id")

# TERCEIRA EXTENSÃO
# tentativa de criar um histograma como o do NetLogo, mas aparentemente 
# não é trivial; os valores a exibir não podem ser listas ou arrays; 
# assim, optei por fixar em 5 o número de segmentos do histograma, mas isso
# aparentemente não é parametrizável e, portanto, não é uma boa solução
hist_reward_agents = BarChartModule([{"Label": "Bin0", "Color": "Blue"},
                             {"Label": "Bin1", "Color": "Blue"},
                             {"Label": "Bin2", "Color": "Blue"},
                             {"Label": "Bin3", "Color": "Blue"},
                             {"Label": "Bin4", "Color": "Blue"}],
                            scope = "model")

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
                       [crowded_element, grid, chart, reward_element, 
                        hist_agents_reward, hist_reward_agents],
                       "El Farol Model",
                       model_params)

# porta 8521 é a porta default
server.launch(port = 8561)
