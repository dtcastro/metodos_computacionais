"""
Roda a simulação do modelo, mas sem exibir os agentes em um grid no browser.
"""

from model import DLAModel

################# pra rodar sem o batch runner ##############
wiggle_angle = 60
number_particles = 2500
probability_of_sticking = 1
neighbor_influence = False
num_seeds = 1
model = DLAModel(wiggle_angle, number_particles, probability_of_sticking, 
                 neighbor_influence, num_seeds)

for i in range(50):
    """ 
    Roda n passos na simulação.
    """
    print('Rodada ' + str(i))
    model.step()

# Recupera os valores finais do coletor de dados
#model_data = model.datacollector.get_model_vars_dataframe()